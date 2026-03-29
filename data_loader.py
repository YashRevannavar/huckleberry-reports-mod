import csv
import pandas as pd
from datetime import datetime
from typing import List, Tuple
from enums import ActivityType, FeedType, DiaperCondition
from models import ActivityRecord
import re

class DataLoader:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DataLoader, cls).__new__(cls)
        return cls._instance

    def _parse_time(self, time_str: str) -> datetime:
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
            return float(parts[0]) * 60 + float(parts[1])
        return 0.0

    def _extract_amount(self, value: str) -> float:
        if not value:
            return 0.0
        match = re.search(r'([\d.]+)', value)
        return float(match.group(1)) if match else 0.0

    def load_data(self, file_path: str) -> Tuple[List[ActivityRecord], pd.DataFrame]:
        records = []
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
        df['activity_type'] = df['activity_type'].apply(lambda x: x.value)
        df['feed_type'] = df['feed_type'].apply(lambda x: x.value)
        
        return records, df

# Singleton instance access
data_loader = DataLoader()
