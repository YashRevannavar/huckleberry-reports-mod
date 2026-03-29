#!/bin/bash
# A simple script to activate the virtual environment and test run.py

echo "Activating virtual environment..."
source backend/.venv/bin/activate

echo "Running report generation..."
python run.py ./data/Huckleberry-28-march.csv

echo "Done! Check the reports/ folder for the output PDF."
