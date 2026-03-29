import pandas as pd
from typing import List

from backend.utilities.logging_config import setup_logger
from backend.utilities.models import Result
from .models import DailyKPIs
from .analytics_handler import AnalyticsHandler

logger = setup_logger(__name__)

class AnalyticsService:
    def __init__(self):
        self.handler = AnalyticsHandler()

    def calculate_kpis(self, df: pd.DataFrame) -> Result[List[DailyKPIs]]:
        """
        Orchestrates KPI calculation pipeline from source DataFrames.
        :param df: Clean pandas DataFrame context.
        :return: Result wrapping a list of computed DailyKPIs.
        """
        logger.info("Initializing analytics calculation...")
        result = self.handler.calculate_daily_kpis(df)
        if result.success and result.data is not None:
            # Sort chronologically as a standardized layer requirement
            result.data.sort(key=lambda k: k.date)
        return result
