from typing import List, Dict

from backend.utilities.logging_config import setup_logger
from backend.utilities.models import Result
from backend.analytics.models import DailyKPIs
from backend.data_processing.enums import ActivityType
from .chart_handler import ChartHandler

logger = setup_logger(__name__)

class ChartService:
    def __init__(self):
        self.handler = ChartHandler()

    def generate_all_charts(self, kpis: List[DailyKPIs], temp_dir: str) -> Result[Dict[str, str | List[str]]]:
        """
        Orchestrates plotting workflow, aggregating outputs cleanly.
        :param kpis: Computed statistics.
        :param temp_dir: Directory where png charts are stored correctly.
        """
        logger.info(f"Generating charts into {temp_dir}...")
        results = {}

        feed_res = self.handler.generate_feed_volume_chart(kpis, temp_dir)
        diaper_res = self.handler.generate_diaper_chart(kpis, temp_dir)
        temp_res = self.handler.generate_temp_chart(kpis, temp_dir)
        growth_res = self.handler.generate_growth_chart(kpis, temp_dir)

        if not (feed_res.success and diaper_res.success and temp_res.success and growth_res.success):
            return Result(success=False, error="One or more core charts failed to build.")

        results['feed'] = feed_res.data
        results['diaper'] = diaper_res.data
        results['temp'] = temp_res.data
        results['growth'] = growth_res.data

        # Heatmaps
        heatmap_paths = []
        heat_acts = [ActivityType.TUMMY_TIME.value]
        for act in heat_acts:
            hm_res = self.handler.generate_calendar_heatmap(kpis, act, f"{act} Daily Tracker", temp_dir)
            if hm_res.success and hm_res.data:
                heatmap_paths.append(hm_res.data)
                
        results['heatmaps'] = heatmap_paths
        
        logger.info("Successfully generated all charts")
        return Result(success=True, data=results)
