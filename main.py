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
6. visualization.py - Creates all charts
"""

import filter
import data_cleaning
import statistical_analysis
import text_analysis
import advanced_features_analysis
import visualization

print("\n" + "=" * 70)
print("✅ ALL TASKS COMPLETED SUCCESSFULLY!")
print("=" * 70)
print("""
📁 OUTPUT FILES CREATED:
   - datasets/filtered_data.csv
   - datasets/cleaned_accidents.csv
   - outputs/tables/*.csv (25+ files)
   - outputs/figures/*.png (13 charts)
   - outputs/reports/*.txt
""")
print("=" * 70)