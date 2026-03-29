# Baby Analytics Report Generator

A high-fidelity, visually professional PDF report generator designed to transform raw Huckleberry baby tracking CSV data into actionable health insights. Built with Python, Jinja2, Tailwind CSS, Playwright, and Matplotlib.

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
# Create and activate virtual environment inside backend
python3 -m venv backend/.venv
source backend/.venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browser binaries
playwright install chromium
```

### 3. Configuration
Create a `.env` file in the root directory (referencing `.env.example`):
```bash
BABY_NAME="Ekavira Revannavar"
BABY_DOB="13-03-2024"
```

### 4. Running the Report
Place your Huckleberry CSV export in the `data/` folder and run from the root:
```bash
python run.py data/Huckleberry-28-march.csv --output reports/Baby_Analytics_Report.pdf
```
Alternatively, just run the built-in test wrapper:
```bash
./test.sh
```

## 🛠 Project Structure (Backend)

We follow standard Python structural principles using modular Service-and-Handler paradigms with explicit DTOs.

- `backend/main.py`: Entry orchestration orchestrating cleanly divided workflows.
- `backend/utilities/`: Root `.env` references, general error-safe `Result` wrappers, and centralized `logging_config.py`.
- `backend/data_processing/`: Feature pipeline parsing CSVs directly into strict `ActivityRecord` DTO lists.
- `backend/analytics/`: Calculating aggregated `DailyKPIs` matrices over DataFrames.
- `backend/charting/`: Abstracted logic building seaborn/matplotlib themed charts.
- `backend/reporting/`: Handlers tying charting references into Playwright HTML-PDF builds.

*Created with ❤️ for Ekavira.*
