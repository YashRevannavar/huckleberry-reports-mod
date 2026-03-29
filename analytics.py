import pandas as pd
from typing import List
from models import DailyKPIs
from enums import ActivityType, FeedType, DiaperCondition

class AnalyticsEngine:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AnalyticsEngine, cls).__new__(cls)
        return cls._instance

    def calculate_daily_kpis(self, df: pd.DataFrame) -> List[DailyKPIs]:
        df['date'] = df['start_time'].dt.date
        kpis = []

        # Process diapers to determine exact type
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
            
            diapers['diaper_type'] = diapers['diaper_condition'].apply(determine_diaper_type)
            pee_count = sum(diapers['diaper_type'] == DiaperCondition.PEE.value)
            poo_count = sum(diapers['diaper_type'] == DiaperCondition.POO.value)
            both_count = sum(diapers['diaper_type'] == DiaperCondition.BOTH.value)

            # Sleep
            sleeps = group[group['activity_type'] == ActivityType.SLEEP.value]
            sleep_hours = sleeps['duration_minutes'].sum() / 60.0

            # Temperature
            temps = group[group['activity_type'] == ActivityType.TEMP.value]
            avg_temp = temps['temperature'].mean() if not temps.empty else 0.0

            # Growth
            growths = group[group['activity_type'] == ActivityType.GROWTH.value]
            # Use max weight of the day
            weight = growths['weight_kg'].max() if not growths.empty else 0.0

            # Custom Activities duration aggregations (e.g. Tummy time, Bath)
            custom_activities = {}
            for act_name, act_group in group.groupby('activity_type'):
                durations = act_group['duration_minutes'].dropna()
                if not durations.empty:
                    custom_activities[act_name] = round(durations.sum(), 2)

            kpis.append(DailyKPIs(
                date=str(date),
                total_feed_volume_ml=total_feed_volume,
                total_breast_milk_ml=breast_milk_vol,
                total_formula_ml=formula_vol,
                diaper_changes_count=diaper_count,
                pee_diapers_count=pee_count,
                poo_diapers_count=poo_count,
                both_diapers_count=both_count,
                sleep_duration_hours=sleep_hours,
                avg_temp_c=avg_temp,
                weight_kg=weight,
                custom_activities=custom_activities
            ))

        return kpis

# Singleton instance
analytics_engine = AnalyticsEngine()
