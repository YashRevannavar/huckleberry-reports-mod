from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict
from enums import ActivityType, FeedType

@dataclass
class ActivityRecord:
    activity_type: ActivityType
    start_time: datetime
    end_time: Optional[datetime]
    duration_minutes: Optional[float]
    feed_type: FeedType
    feed_amount_ml: Optional[float]
    diaper_condition: str
    temperature: Optional[float]
    weight_kg: Optional[float]
    notes: str

@dataclass
class DailyKPIs:
    date: str
    total_feed_volume_ml: float
    total_breast_milk_ml: float
    total_formula_ml: float
    diaper_changes_count: int
    pee_diapers_count: int
    poo_diapers_count: int
    both_diapers_count: int
    sleep_duration_hours: float
    avg_temp_c: float
    weight_kg: float
    custom_activities: Dict[str, float] = field(default_factory=dict)

    def __post_init__(self):
        self.total_feed_volume_ml = round(self.total_feed_volume_ml, 2)
        self.total_breast_milk_ml = round(self.total_breast_milk_ml, 2)
        self.total_formula_ml = round(self.total_formula_ml, 2)
        self.sleep_duration_hours = round(self.sleep_duration_hours, 2)
        self.avg_temp_c = round(self.avg_temp_c, 2)
        self.weight_kg = round(self.weight_kg, 2)
