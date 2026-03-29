import sys
import os
import argparse

# Ensure the root directory is on the path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from backend.main import main

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate visually modern reports from Huckleberry CSV.")
    parser.add_argument('csv_path', type=str, help='Path to the input CSV file')
    parser.add_argument('--output', type=str, default='reports/Baby_Analytics_Report.pdf', help='Path to output PDF')
    
    args = parser.parse_args()
    main(args.csv_path, args.output)
