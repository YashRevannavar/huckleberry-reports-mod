# Baby Analytics Report Generator

A high-fidelity, visually professional PDF report generator designed to transform raw Huckleberry baby tracking CSV data into actionable health insights. Built with Python, Jinja2, Tailwind CSS, and Playwright.

## ✨ Features

- **Velocity Board**: Instant snapshot of Today, Yesterday, and 3-Day Average for Feeding, Diapers, Temperature, and Weight.
- **Modern Visualizations**: 
    - Feeding Volume Trends (Breast Milk vs. Formula).
    - Diaper Output History (Pee/Poo split).
    - Body Temperature Analysis.
    - Growth & Weight Tracker.
- **GitHub-style Heatmaps**: Reusable contribution-style grids to track daily activities like **Tummy Time**.
- **Premium Aesthetics**: Styled with the **Catppuccin Latte** theme and modern **Space Grotesk** typography.
- **Print Optimized**: Specifically designed as a 2-page PDF dashboard with intelligent page-break management.

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10+
- [Playwright](https://playwright.dev/python/) for PDF rendering.

### 2. Installation
Clone the repository and set up the environment:
```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browser binaries
playwright install chromium
```

### 3. Configuration
Create a `.env` file in the root directory (referencing `.env.example`):
```bash
BABY_NAME="Ekavira Revannavar"
BABY_DOB="13-03-2026"
```

### 4. Running the Report
Place your Huckleberry CSV export in the `data/` folder and run:
```bash
python main.py data/your_export.csv --output reports/My_Baby_Report.pdf
```

## 🛠 Project Structure
- `main.py`: Entry point for the pipeline.
- `analytics.py`: Logic for calculating daily KPIs and custom activity aggregations.
- `charts.py`: Matplotlib/Seaborn engine for generating themed charts and heatmaps.
- `report_builder.py`: HTML-to-PDF rendering engine using Playwright.
- `report_template.html`: Modern Tailwind CSS layout definition.
- `data_loader.py`: Robust CSV parser for Huckleberry exports.

## 🧩 Customization
To add more activity heatmaps (e.g., for "Bath" or "Sleep"), update the `heat_acts` list in `main.py`:
```python
heat_acts = [ActivityType.TUMMY_TIME.value, ActivityType.BATH.value]
```

---
*Created with ❤️ for Ekavira.*
