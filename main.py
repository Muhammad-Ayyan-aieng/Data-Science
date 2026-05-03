# main.py
"""
US Accidents Analysis - Main Controller
AINE 312 Term Project - States: GA and CT

This script runs all analysis modules in sequence:
1. filter.py - Filters raw data to GA & CT
2. data_cleaning.py - Cleans the filtered data
3. statistical_analysis.py - Basic statistics
4. text_analysis.py - NLP on descriptions
5. advanced_features_analysis.py - Road features, geography
6. comparison_analysis.py - GA vs CT comparative analysis
7. visualization.py - Creates all charts
"""

import filter
import data_cleaning
import statistical_analysis
import text_analysis
import advanced_features_analysis
import comparison_analysis
import visualization

print("\n" + "=" * 80)
print("✅ ALL TASKS COMPLETED SUCCESSFULLY!")
print("=" * 80)
print("""
📁 OUTPUT FILES CREATED:

DATASETS:
   - datasets/filtered_data.csv
   - datasets/cleaned_accidents.csv

STATISTICAL ANALYSIS (outputs/statistical_analysis/):
   ├── tables/ (11 CSV files)
   └── reports/ (Excel + Word)

TEXT ANALYSIS (outputs/text_analysis/):
   ├── tables/ (4 CSV files)
   └── reports/ (Excel + Word)

ADVANCED FEATURES (outputs/advanced_features/):
   ├── tables/ (8 CSV files)
   └── reports/ (Excel + Word)

COMPARISON ANALYSIS (outputs/comparison_analysis/):
   ├── tables/ (8 CSV files)
   └── reports/ (Excel + Word)

VISUALIZATION (outputs/figures/):
   └── 11 PNG charts

📊 Total files created: 30+ CSV, 4 Excel, 4 Word, 11 PNG
""")
print("=" * 80)