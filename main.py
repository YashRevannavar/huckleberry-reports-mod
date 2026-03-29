import os
import argparse
from data_loader import data_loader
from analytics import analytics_engine
from charts import chart_generator
from report_builder import report_builder

def main(csv_path: str, output_pdf: str):
    if not os.path.exists(csv_path):
        print(f"Error: File '{csv_path}' does not exist.")
        return

    print("Loading data...")
    records, df = data_loader.load_data(csv_path)
    print(f"Loaded {len(records)} records.")

    print("Calculating analytics...")
    kpis = analytics_engine.calculate_daily_kpis(df)
    
    # Sort KPIs chronologically
    kpis.sort(key=lambda k: k.date)

    print("Generating charts...")
    temp_dir = os.path.join(os.path.dirname(__file__), 'temp_reports')
    
    feed_chart_path = chart_generator.generate_feed_volume_chart(kpis, temp_dir)
    diaper_chart_path = chart_generator.generate_diaper_chart(kpis, temp_dir)
    temp_chart_path = chart_generator.generate_temp_chart(kpis, temp_dir)
    growth_chart_path = chart_generator.generate_growth_chart(kpis, temp_dir)

    # Generate reusable Heatmaps for chosen activity enums
    heatmap_paths = []
    from enums import ActivityType
    heat_acts = [ActivityType.TUMMY_TIME.value]
    for act in heat_acts:
        path = chart_generator.generate_calendar_heatmap(kpis, act, f"{act} Daily Tracker", temp_dir)
        if path:
            heatmap_paths.append(path)

    print("Building modern PDF report...")
    report_opts = {
        'feed': feed_chart_path,
        'diaper': diaper_chart_path,
        'temp': temp_chart_path,
        'growth': growth_chart_path,
        'heatmaps': heatmap_paths
    }
    
    os.makedirs(os.path.dirname(output_pdf) if os.path.dirname(output_pdf) else '.', exist_ok=True)
    report_builder.generate_pdf(kpis, report_opts, output_pdf)
    
    print(f"Report successfully generated at: {output_pdf}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate visually modern reports from Huckleberry CSV.")
    parser.add_argument('csv_path', type=str, help='Path to the input CSV file')
    parser.add_argument('--output', type=str, default='reports/Baby_Analytics_Report.pdf', help='Path to output PDF')
    
    args = parser.parse_args()
    
    main(args.csv_path, args.output)
