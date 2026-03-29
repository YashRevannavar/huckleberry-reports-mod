import csv
import pandas as pd
from datetime import datetime
from typing import List, Tuple, Optional
import re

from backend.utilities.logging_config import setup_logger
from backend.utilities.models import Result
from .enums import ActivityType, FeedType
from .models import ActivityRecord
from .contracts import BaseDataLoader

logger = setup_logger(__name__)

class DataHandler(BaseDataLoader):
    
    def _parse_time(self, time_str: str) -> Optional[datetime]:
        if not time_str:
            return None
        try:
            return datetime.strptime(time_str, "%Y-%m-%d %H:%M")
        except ValueError:
            return None
            
    def _parse_duration(self, duration_str: str) -> float:
        if not duration_str or ":" not in duration_str:
            return 0.0
        parts = duration_str.split(":")
        if len(parts) == 2:
            try:
                return float(parts[0]) * 60 + float(parts[1])
            except ValueError:
                return 0.0
        return 0.0

    def _extract_amount(self, value: str) -> float:
        if not value:
            return 0.0
        match = re.search(r'([\d.]+)', value)
        if match:
            try:
                return float(match.group(1))
            except ValueError:
                return 0.0
        return 0.0

    def load_data(self, file_path: str) -> Result[Tuple[List[ActivityRecord], pd.DataFrame]]:
        records = []
        try:
            with open(file_path, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    activity_type = ActivityType.from_string(row.get('Type', ''))
                    start_time = self._parse_time(row.get('Start', ''))
                    end_time = self._parse_time(row.get('End', ''))
                    
                    # Default nulls
                    duration = 0.0
                    feed_type = FeedType.UNKNOWN
                    feed_amount_ml = 0.0
                    diaper_condition = ""
                    temperature = 0.0
                    weight_kg = 0.0
                    
                    if activity_type == ActivityType.FEED:
                        feed_type = FeedType.from_string(row.get('Start Condition', ''))
                        feed_amount_ml = self._extract_amount(row.get('End Condition', ''))
                    elif activity_type == ActivityType.DIAPER:
                        diaper_condition = row.get('End Condition', '')
                    elif activity_type == ActivityType.GROWTH:
                        weight_kg = self._extract_amount(row.get('Start Condition', ''))
                    elif activity_type == ActivityType.TEMP:
                        temperature = self._extract_amount(row.get('Start Condition', ''))
                    elif activity_type in [ActivityType.SLEEP, ActivityType.TUMMY_TIME, ActivityType.BATH]:
                        duration = self._parse_duration(row.get('Duration', ''))

                    record = ActivityRecord(
                        activity_type=activity_type,
                        start_time=start_time,
                        end_time=end_time,
                        duration_minutes=duration,
                        feed_type=feed_type,
                        feed_amount_ml=feed_amount_ml,
                        diaper_condition=diaper_condition,
                        temperature=temperature,
                        weight_kg=weight_kg,
                        notes=row.get('Notes', '')
                    )
                    records.append(record)

            # Create DataFrame
            df = pd.DataFrame([r.__dict__ for r in records])
            # Convert enums to string for easier pandas querying
            if not df.empty:
                df['activity_type'] = df['activity_type'].apply(lambda x: x.value)
                df['feed_type'] = df['feed_type'].apply(lambda x: x.value)
                
            logger.info(f"Successfully loaded {len(records)} records from {file_path}")
            return Result(success=True, data=(records, df))
            
        except FileNotFoundError:
            error_msg = f"File not found: {file_path}"
            logger.error(error_msg)
            return Result(success=False, error=error_msg)
        except Exception as e:
            error_msg = f"Failed to parse data from {file_path}. Error: {str(e)}"
            logger.exception(error_msg)
            return Result(success=False, error=error_msg)
