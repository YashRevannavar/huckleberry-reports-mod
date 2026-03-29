import pandas as pd
from typing import List

from backend.utilities.logging_config import setup_logger
from backend.utilities.models import Result
from backend.data_processing.enums import ActivityType, FeedType, DiaperCondition
from .models import DailyKPIs

logger = setup_logger(__name__)

class AnalyticsHandler:
    def calculate_daily_kpis(self, df: pd.DataFrame) -> Result[List[DailyKPIs]]:
        try:
            if df.empty:
                return Result(success=True, data=[])

            # Ensure start_time is datetime if not already
            if not pd.api.types.is_datetime64_any_dtype(df['start_time']):
                df['start_time'] = pd.to_datetime(df['start_time'])

            df['date'] = df['start_time'].dt.date
            kpis = []

            def determine_diaper_type(cond):
                if not isinstance(cond, str):
                    return DiaperCondition.UNKNOWN.value
                return DiaperCondition.from_string(cond).value

            for date, group in df.groupby('date'):
                # Feeds
                feeds = group[group['activity_type'] == ActivityType.FEED.value]
                total_feed_volume = feeds['feed_amount_ml'].sum()
                breast_milk_vol = feeds[feeds['feed_type'] == FeedType.BREAST_MILK.value]['feed_amount_ml'].sum()
                formula_vol = feeds[feeds['feed_type'] == FeedType.FORMULA.value]['feed_amount_ml'].sum()

                # Diapers
                diapers = group[group['activity_type'] == ActivityType.DIAPER.value].copy()
                diaper_count = len(diapers)
                
                if diaper_count > 0:
                    diapers['diaper_type'] = diapers['diaper_condition'].apply(determine_diaper_type)
                    pee_count = sum(diapers['diaper_type'] == DiaperCondition.PEE.value)
                    poo_count = sum(diapers['diaper_type'] == DiaperCondition.POO.value)
                    both_count = sum(diapers['diaper_type'] == DiaperCondition.BOTH.value)
                else:
                    pee_count = poo_count = both_count = 0

                # Sleep
                sleeps = group[group['activity_type'] == ActivityType.SLEEP.value]
                sleep_hours = sleeps['duration_minutes'].sum() / 60.0

                # Temperature
                temps = group[group['activity_type'] == ActivityType.TEMP.value]
                avg_temp = temps['temperature'].mean() if not temps.empty else 0.0

                # Growth (Weight) -> max for the day
                growths = group[group['activity_type'] == ActivityType.GROWTH.value]
                weight = growths['weight_kg'].max() if not growths.empty else 0.0

                # Custom Activities
                custom_activities = {}
                for act_name, act_group in group.groupby('activity_type'):
                    durations = act_group['duration_minutes'].dropna()
                    if not durations.empty:
                        custom_activities[act_name] = round(durations.sum(), 2)

                kpis.append(DailyKPIs(
                    date=str(date),
                    total_feed_volume_ml=float(total_feed_volume),
                    total_breast_milk_ml=float(breast_milk_vol),
                    total_formula_ml=float(formula_vol),
                    diaper_changes_count=int(diaper_count),
                    pee_diapers_count=int(pee_count),
                    poo_diapers_count=int(poo_count),
                    both_diapers_count=int(both_count),
                    sleep_duration_hours=float(sleep_hours),
                    avg_temp_c=float(avg_temp),
                    weight_kg=float(weight),
                    custom_activities=custom_activities
                ))

            logger.info(f"Successfully calculated KPIs for {len(kpis)} days.")
            return Result(success=True, data=kpis)

        except Exception as e:
            error_msg = f"Failed to calculate analytics: {str(e)}"
            logger.exception(error_msg)
            return Result(success=False, error=error_msg)
