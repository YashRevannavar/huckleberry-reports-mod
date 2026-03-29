import os
import argparse
import sys

from backend.utilities.logging_config import setup_logger
from backend.data_processing.data_service import DataService
from backend.analytics.analytics_service import AnalyticsService
from backend.charting.chart_service import ChartService
from backend.reporting.report_service import ReportService

logger = setup_logger(__name__)

def main(csv_path: str, output_pdf: str):
    logger.info("=====================================")
    logger.info(" Starting Huckleberry Report Builder")
    logger.info("=====================================")

    # 1. Data Processing
    data_service = DataService()
    data_res = data_service.fetch_parsed_data(csv_path)
    if not data_res.success or not data_res.data:
        logger.error(f"Data Load Failed: {data_res.error}")
        sys.exit(1)
        
    records, df = data_res.data
    logger.info("Data processed successfully.")

    # 2. Analytics
    analytics_service = AnalyticsService()
    kpis_res = analytics_service.calculate_kpis(df)
    if not kpis_res.success or not kpis_res.data:
        logger.error(f"KPIs Calculation Failed: {kpis_res.error}")
        sys.exit(1)
        
    kpis = kpis_res.data
    logger.info("Analytics calculated successfully.")

    # 3. Charting
    chart_service = ChartService()
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    temp_dir = os.path.join(project_root, 'temp_reports')
    
    charts_res = chart_service.generate_all_charts(kpis, temp_dir)
    if not charts_res.success or not charts_res.data:
        logger.error(f"Chart Generation Failed: {charts_res.error}")
        sys.exit(1)
        
    chart_paths = charts_res.data
    logger.info("Charts built successfully.")

    # 4. Reporting
    report_service = ReportService()
    report_res = report_service.generate_report(kpis, chart_paths, output_pdf)
    if not report_res.success:
        logger.error(f"Report Render Failed: {report_res.error}")
        sys.exit(1)

    logger.info("=====================================")
    logger.info(f"Report Successfully Saved: {output_pdf}")
    logger.info("=====================================")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate visually modern reports from Huckleberry CSV.")
    parser.add_argument('csv_path', type=str, help='Path to the input CSV file')
    parser.add_argument('--output', type=str, default='reports/Baby_Analytics_Report.pdf', help='Path to output PDF')
    
    args = parser.parse_args()
    main(args.csv_path, args.output)
