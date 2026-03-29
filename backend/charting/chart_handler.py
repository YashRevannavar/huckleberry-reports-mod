import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List

from backend.utilities.logging_config import setup_logger
from backend.utilities.models import Result
from backend.analytics.models import DailyKPIs
from .contracts import BaseChartGenerator

logger = setup_logger(__name__)

# Catppuccin Latte (Light) Palette Options
c_base = "#eff1f5"
c_text = "#4c4f69"
c_subtext = "#6c6f85"
c_surface0 = "#ccd0da"
c_blue = "#1e66f5"
c_pink = "#ea76cb"
c_yellow = "#df8e1d"
c_peach = "#fe640b"
c_green = "#40a02b"
c_red = "#d20f39"
c_teal = "#179299"
c_mauve = "#8839ef"

class ChartHandler(BaseChartGenerator):
    def __init__(self):
        # Setup Catppuccin Latte styling for charts
        plt.rcParams['font.size'] = 16
        plt.rcParams['axes.titlesize'] = 20
        plt.rcParams['axes.labelsize'] = 16
        plt.rcParams['xtick.labelsize'] = 14
        plt.rcParams['ytick.labelsize'] = 14
        plt.rcParams['legend.fontsize'] = 14
        
        plt.rcParams['axes.facecolor'] = c_surface0
        plt.rcParams['figure.facecolor'] = c_base
        plt.rcParams['text.color'] = c_text
        plt.rcParams['axes.labelcolor'] = c_text
        plt.rcParams['xtick.color'] = c_subtext
        plt.rcParams['ytick.color'] = c_subtext
        plt.rcParams['axes.edgecolor'] = c_surface0
        plt.rcParams['grid.color'] = "#bcc0cc" # surface1 for subtle grid
        
        sns.set_theme(style="whitegrid", rc=plt.rcParams)

    def _ensure_dir(self, directory: str):
        if not os.path.exists(directory):
            os.makedirs(directory)

    def generate_feed_volume_chart(self, kpis: List[DailyKPIs], output_dir: str) -> Result[str]:
        try:
            self._ensure_dir(output_dir)
            dates = [kpi.date for kpi in kpis]
            breast_milk = [kpi.total_breast_milk_ml for kpi in kpis]
            formula = [kpi.total_formula_ml for kpi in kpis]

            df = pd.DataFrame({'Date': dates, 'Breast Milk (ml)': breast_milk, 'Formula (ml)': formula})
            df = df.sort_values(by='Date')

            # Shorter height to fit dynamically into 2 pages
            fig, ax = plt.subplots(figsize=(10, 3.8))
            fig.patch.set_facecolor(c_base)
            ax.set_facecolor(c_base)
            
            df.plot(x='Date', kind='bar', stacked=True, color=[c_mauve, c_blue], ax=ax)
            
            plt.title('Daily Feed Volume (ml)', fontweight='bold', color=c_text, pad=10)
            plt.xlabel('Date')
            plt.ylabel('Volume (ml)')
            plt.xticks(rotation=45, ha='right')
            plt.legend(facecolor=c_surface0, edgecolor=c_surface0, labelcolor=c_text)
            plt.tight_layout()

            filepath = os.path.join(output_dir, 'feed_volume.png')
            plt.savefig(filepath, dpi=300, facecolor=fig.get_facecolor(), transparent=True)
            plt.close()
            return Result(success=True, data=filepath)
        except Exception as e:
            logger.exception("Failed to generate feed volume chart.")
            return Result(success=False, error=str(e))

    def generate_diaper_chart(self, kpis: List[DailyKPIs], output_dir: str) -> Result[str]:
        try:
            self._ensure_dir(output_dir)
            dates = [kpi.date for kpi in kpis]
            pee = [kpi.pee_diapers_count for kpi in kpis]
            poo = [kpi.poo_diapers_count for kpi in kpis]
            both = [kpi.both_diapers_count for kpi in kpis]

            df = pd.DataFrame({
                'Date': dates,
                'Pee Only': pee,
                'Poo Only': poo,
                'Both': both
            })
            df = df.sort_values(by='Date')

            # Shorter height to fit dynamically into 2 pages
            fig, ax = plt.subplots(figsize=(10, 3.8))
            fig.patch.set_facecolor(c_base)
            ax.set_facecolor(c_base)
            
            df.plot(x='Date', kind='bar', stacked=True, color=[c_yellow, c_peach, c_teal], ax=ax)
            
            plt.title('Diaper Types Breakdown', fontweight='bold', color=c_text, pad=10)
            plt.xlabel('Date')
            plt.ylabel('Count')
            plt.xticks(rotation=45, ha='right')
            plt.legend(title='Condition', facecolor=c_surface0, edgecolor=c_surface0, labelcolor=c_text)
            plt.tight_layout()

            filepath = os.path.join(output_dir, 'diapers.png')
            plt.savefig(filepath, dpi=300, facecolor=fig.get_facecolor(), transparent=True)
            plt.close()
            return Result(success=True, data=filepath)
        except Exception as e:
            logger.exception("Failed to generate diaper chart.")
            return Result(success=False, error=str(e))

    def generate_temp_chart(self, kpis: List[DailyKPIs], output_dir: str) -> Result[str]:
        try:
            self._ensure_dir(output_dir)
            data = [{'Date': k.date, 'Temp': k.avg_temp_c} for k in kpis if k.avg_temp_c > 0]
            if not data:
                return Result(success=True, data="")

            df = pd.DataFrame(data).sort_values(by='Date')

            fig, ax = plt.subplots(figsize=(10, 3.5))
            fig.patch.set_facecolor(c_base)
            ax.set_facecolor(c_base)
            
            ax.plot(df['Date'], df['Temp'], marker='o', color=c_red, linewidth=2, markersize=8)
            ax.fill_between(df['Date'], df['Temp'] - 0.2, df['Temp'] + 0.2, color=c_red, alpha=0.15)
            
            plt.title('Average Daily Temperature (°C)', fontweight='bold', color=c_text, pad=10)
            plt.xlabel('Date')
            plt.ylabel('Temp °C')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()

            filepath = os.path.join(output_dir, 'temp.png')
            plt.savefig(filepath, dpi=300, facecolor=fig.get_facecolor(), transparent=True)
            plt.close()
            return Result(success=True, data=filepath)
        except Exception as e:
            logger.exception("Failed to generate temp chart.")
            return Result(success=False, error=str(e))

    def generate_growth_chart(self, kpis: List[DailyKPIs], output_dir: str) -> Result[str]:
        try:
            self._ensure_dir(output_dir)
            data = [{'Date': k.date, 'Weight': k.weight_kg} for k in kpis if k.weight_kg > 0]
            if not data:
                return Result(success=True, data="")

            df = pd.DataFrame(data).sort_values(by='Date')

            fig, ax = plt.subplots(figsize=(10, 3.5))
            fig.patch.set_facecolor(c_base)
            ax.set_facecolor(c_base)
            
            ax.plot(df['Date'], df['Weight'], marker='o', color=c_green, linewidth=2, markersize=8)
            
            plt.title('Growth Trend (Weight in Kg)', fontweight='bold', color=c_text, pad=10)
            plt.xlabel('Date')
            plt.ylabel('Weight (Kg)')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()

            filepath = os.path.join(output_dir, 'growth.png')
            plt.savefig(filepath, dpi=300, facecolor=fig.get_facecolor(), transparent=True)
            plt.close()
            return Result(success=True, data=filepath)
        except Exception as e:
            logger.exception("Failed to generate growth chart.")
            return Result(success=False, error=str(e))

    def generate_calendar_heatmap(self, kpis: List[DailyKPIs], activity_key: str, title: str, output_dir: str) -> Result[str]:
        try:
            self._ensure_dir(output_dir)
            import numpy as np
            from matplotlib.colors import LinearSegmentedColormap
            
            data_dict = {k.date: k.custom_activities.get(activity_key, 0.0) for k in kpis}
            if not data_dict:
                return Result(success=True, data="")

            dates = pd.to_datetime(list(data_dict.keys()))
            if dates.empty:
                return Result(success=True, data="")

            min_date, max_date = dates.min(), dates.max()
            start_date = min_date - pd.Timedelta(days=min_date.weekday())
            end_date = max_date + pd.Timedelta(days=6 - max_date.weekday())
            
            all_dates = pd.date_range(start_date, end_date)
            df_cal = pd.DataFrame(index=all_dates)
            df_cal['duration'] = [data_dict.get(d.strftime('%Y-%m-%d'), 0.0) for d in all_dates]
            
            df_cal['day_of_week'] = df_cal.index.weekday
            df_cal['week'] = ((df_cal.index - start_date).days // 7)
            
            matrix = df_cal.pivot(index='day_of_week', columns='week', values='duration')
            
            fig, ax = plt.subplots(figsize=(max(6, int(matrix.shape[1] * 0.5)), 2.5))
            fig.patch.set_facecolor(c_base)
            ax.set_facecolor(c_base)

            cmap = LinearSegmentedColormap.from_list('cat_green', [c_surface0, c_teal, c_green])
            
            sns.heatmap(matrix, cmap=cmap, linewidths=2, linecolor=c_base, 
                        cbar=False, ax=ax, square=True)

            ax.set_yticks([0.5, 2.5, 4.5, 6.5])
            ax.set_yticklabels(['Mon', 'Wed', 'Fri', 'Sun'], rotation=0, fontsize=10)
            ax.set_xticks([]) 
            
            plt.title(title, fontweight='bold', color=c_text, pad=10, fontsize=16)
            plt.xlabel('')
            plt.ylabel('')
            plt.tight_layout()

            filename = f"{activity_key.lower().replace(' ', '_')}_heatmap.png"
            filepath = os.path.join(output_dir, filename)
            plt.savefig(filepath, dpi=300, facecolor=fig.get_facecolor(), transparent=True)
            plt.close()
            return Result(success=True, data=filepath)
        except Exception as e:
            logger.exception(f"Failed to generate heatmap for {activity_key}")
            return Result(success=False, error=str(e))
