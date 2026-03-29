from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from .enums import ActivityType, FeedType

@dataclass
class ActivityRecord:
    activity_type: ActivityType
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    duration_minutes: float
    feed_type: FeedType
    feed_amount_ml: float
    diaper_condition: str
    temperature: float
    weight_kg: float
    notes: str
