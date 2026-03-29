import os
import base64
from typing import List, Dict, Any
from jinja2 import Environment, FileSystemLoader
from playwright.sync_api import sync_playwright
from datetime import datetime
from dateutil.relativedelta import relativedelta

from backend.utilities.logging_config import setup_logger
from backend.utilities.models import Result
from backend.utilities.constants import BABY_NAME, BABY_DOB
from backend.analytics.models import DailyKPIs

logger = setup_logger(__name__)

class ReportHandler:
    def _encode_image(self, filepath: str) -> str:
        if not filepath or not os.path.exists(filepath):
            return ""
        try:
            with open(filepath, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        except Exception:
            return ""

    def _calculate_age(self, dob_str: str, latest_date_str: str) -> str:
        try:
            dob = datetime.strptime(dob_str, "%d-%m-%Y")
            latest_date = datetime.strptime(latest_date_str, "%Y-%m-%d")
        except ValueError:
            return "Unknown"

        if latest_date < dob:
            return "Not born yet"

        diff = relativedelta(latest_date, dob)
        parts = []
        if diff.years > 0:
            parts.append(f"{diff.years} year{'s' if diff.years != 1 else ''}")
        if diff.months > 0:
            parts.append(f"{diff.months} month{'s' if diff.months != 1 else ''}")
        if diff.days > 0:
            parts.append(f"{diff.days} day{'s' if diff.days != 1 else ''}")

        if not parts:
            return "0 days"
        return ", ".join(parts)

    def _format_metric(self, val: float, suffix: str) -> str:
        return f"{val:.1f} {suffix}" if val > 0 else "not checked"

    def build_pdf(self, kpis: List[DailyKPIs], chart_paths: Dict[str, Any], output_path: str) -> Result[str]:
        try:
            if not kpis:
                return Result(success=False, error="No metrics available to render PDF.")

            today = kpis[-1]
            yesterday = kpis[-2] if len(kpis) > 1 else None
            
            last_3 = kpis[-3:]
            avg_3_feed = sum(k.total_feed_volume_ml for k in last_3) / len(last_3)
            avg_3_diaper = sum(k.diaper_changes_count for k in last_3) / len(last_3)
            
            last_3_temps = [k.avg_temp_c for k in last_3 if k.avg_temp_c > 0]
            avg_3_temp = sum(last_3_temps) / len(last_3_temps) if last_3_temps else 0.0

            last_3_weights = [k.weight_kg for k in last_3 if k.weight_kg > 0]
            avg_3_weight = sum(last_3_weights) / len(last_3_weights) if last_3_weights else 0.0

            dob_str = BABY_DOB
            if not dob_str:
                dob_str = "01-01-2024"

            latest_date_str = today.date
            baby_age = self._calculate_age(dob_str, latest_date_str)

            context = {
                "baby_name": BABY_NAME,
                "baby_dob": dob_str,
                "baby_age": baby_age,
                "today_date": today.date,
                "today_feed": f"{today.total_feed_volume_ml:.0f}",
                "today_diapers": today.diaper_changes_count,
                "yesterday_feed": f"{yesterday.total_feed_volume_ml:.0f}" if yesterday else "0",
                "yesterday_diapers": yesterday.diaper_changes_count if yesterday else "0",
                "avg_3_feed": f"{avg_3_feed:.0f}",
                "avg_3_diaper": f"{avg_3_diaper:.1f}",

                "today_temp": self._format_metric(today.avg_temp_c, "°C"),
                "today_weight": self._format_metric(today.weight_kg, "Kg"),
                "yesterday_temp": self._format_metric(yesterday.avg_temp_c if yesterday else 0, "°C"),
                "yesterday_weight": self._format_metric(yesterday.weight_kg if yesterday else 0, "Kg"),
                "avg_3_temp": self._format_metric(avg_3_temp, "°C"),
                "avg_3_weight": self._format_metric(avg_3_weight, "Kg"),

                "feed_chart_b64": self._encode_image(chart_paths.get('feed', '')),
                "diaper_chart_b64": self._encode_image(chart_paths.get('diaper', '')),
                "temp_chart_b64": self._encode_image(chart_paths.get('temp', '')),
                "growth_chart_b64": self._encode_image(chart_paths.get('growth', '')),
                "activity_heatmaps": [self._encode_image(p) for p in chart_paths.get('heatmaps', [])]
            }

            template_dir = os.path.join(os.path.dirname(__file__), 'templates')
            env = Environment(loader=FileSystemLoader(template_dir))
            template = env.get_template('report_template.html')
            html_content = template.render(context)

            temp_html_path = os.path.join(template_dir, 'temp_rendered_report.html')
            with open(temp_html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)

            os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
            
            with sync_playwright() as p:
                browser = p.chromium.launch(args=['--no-sandbox'])
                page = browser.new_page()
                absolute_html_path = f"file://{os.path.abspath(temp_html_path)}"
                
                page.goto(absolute_html_path, wait_until='networkidle')
                page.pdf(path=output_path, format="A4", print_background=True, margin={"top": "0", "right": "0", "bottom": "0", "left": "0"})
                browser.close()

            if os.path.exists(temp_html_path):
                os.remove(temp_html_path)

            logger.info(f"Report cleanly synthesized into {output_path}")
            return Result(success=True, data=output_path)
        except Exception as e:
            logger.exception("Failed PDF Generation routines")
            return Result(success=False, error=str(e))
