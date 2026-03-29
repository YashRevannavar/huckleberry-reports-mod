from abc import ABC, abstractmethod
from typing import List
from backend.utilities.models import Result
from backend.analytics.models import DailyKPIs

class BaseChartGenerator(ABC):
    """
    Contract outlining methods any Charting implementation must support.
    """
    
    @abstractmethod
    def generate_feed_volume_chart(self, kpis: List[DailyKPIs], output_dir: str) -> Result[str]:
        pass

    @abstractmethod
    def generate_diaper_chart(self, kpis: List[DailyKPIs], output_dir: str) -> Result[str]:
        pass

    @abstractmethod
    def generate_temp_chart(self, kpis: List[DailyKPIs], output_dir: str) -> Result[str]:
        pass

    @abstractmethod
    def generate_growth_chart(self, kpis: List[DailyKPIs], output_dir: str) -> Result[str]:
        pass

    @abstractmethod
    def generate_calendar_heatmap(self, kpis: List[DailyKPIs], activity_key: str, title: str, output_dir: str) -> Result[str]:
        pass
