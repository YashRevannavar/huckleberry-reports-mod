from typing import List, Dict, Any

from backend.utilities.logging_config import setup_logger
from backend.utilities.models import Result
from backend.analytics.models import DailyKPIs
from backend.reporting.report_handler import ReportHandler

logger = setup_logger(__name__)

class ReportService:
    def __init__(self):
        self.handler = ReportHandler()

    def generate_report(self, kpis: List[DailyKPIs], chart_paths: Dict[str, Any], output_pdf: str) -> Result[str]:
        logger.info(f"Kicking off final PDF builder... destination: {output_pdf}")
        
        if not kpis:
            error_msg = "Missing key performance indicators. PDF report aborting."
            logger.error(error_msg)
            return Result(success=False, error=error_msg)
            
        return self.handler.build_pdf(kpis, chart_paths, output_pdf)
