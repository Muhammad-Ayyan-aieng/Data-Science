# statistical_analysis.py
"""
Step 3: Statistical Analysis of Cleaned Accident Data
Calculates central tendency, dispersion, correlations, and categorical distributions
Exports to: 1 Excel file, 1 Word file, multiple CSV files
"""

import pandas as pd
import numpy as np
import os
from scipy import stats
from datetime import datetime

# Optional imports for Excel and Word
try:
    from openpyxl import Workbook
    from openpyxl.styles import Font, Alignment, PatternFill
    HAS_OPENPYXL = True
except ImportError:
    HAS_OPENPYXL = False
    print("⚠️ openpyxl not installed. Excel export limited.")

try:
    from docx import Document
    from docx.shared import Inches, Pt
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    HAS_PYTHON_DOCX = True
except ImportError:
    HAS_PYTHON_DOCX = False
    print("⚠️ python-docx not installed. Word export limited.")

def run_statistical_analysis():
    """Main function to perform statistical analysis on cleaned data"""
    
    print("=" * 70)
    print("📊 STATISTICAL ANALYSIS - GA & CT ACCIDENTS")
    print("=" * 70)
    
    # Create output folders
    os.makedirs("outputs/statistical_analysis/tables", exist_ok=True)
    os.makedirs("outputs/statistical_analysis/reports", exist_ok=True)
    
    # Load data
    input_file = os.path.join("datasets", "cleaned_accidents.csv")
    
    if not os.path.exists(input_file):
        print(f"\n❌ ERROR: {input_file} not found!")
        print("   Please run data_cleaning.py first")
        return None
    
    print(f"\n📂 Loading {input_file}...")
    df = pd.read_csv(input_file)
    print(f"✅ Loaded {len(df):,} accidents")
    print(f"✅ Columns: {len(df.columns)}")
    
    # Date range if available
    if 'Start_Time' in df.columns:
        df['Start_Time'] = pd.to_datetime(df['Start_Time'])
        print(f"📅 Date range: {df['Start_Time'].min().date()} to {df['Start_Time'].max().date()}")
    
    # =========================================================
    # SECTION 1: NUMERICAL FEATURES SUMMARY
    # =========================================================
    print("\n" + "-" * 50)
    print("1. NUMERICAL FEATURES SUMMARY")
    print("-" * 50)
    
    # Define numerical columns (excluding text keywords - those go to text_analysis.py)
    numerical_cols = ['Severity', 'Temperature(F)', 'Humidity(%)', 
                      'Pressure(in)', 'Visibility(mi)', 'Wind_Speed(mph)', 
                      'Precipitation(in)', 'Hour', 'Month', 'DayOfWeek', 
                      'Duration_Minutes']
    
    # Add binary/boolean columns (0/1) - these are statistical features
    binary_cols = ['Junction', 'Traffic_Signal', 'Crossing', 'Railway', 'Stop',
                   'Traffic_Calming', 'Roundabout', 'Amenity', 'Station', 'No_Exit',
                   'IsWeekend', 'Rain_Junction', 'Fog_Night', 'Freezing_Conditions',
                   'Heavy_Rain', 'Low_Visibility', 'Rush_Hour', 'Late_Night',
                   'Dangerous_Intersection', 'Safe_Road']
    
    # Filter existing columns
    available_num = [col for col in numerical_cols if col in df.columns]
    available_binary = [col for col in binary_cols if col in df.columns]
    all_stat_cols = available_num + available_binary
    
    print(f"   Analyzing {len(all_stat_cols)} statistical features")
    
    # Create summary DataFrame
    summary_rows = []
    for col in all_stat_cols:
        if col in df.columns:
            summary_rows.append({
                'Feature': col,
                'Data_Type': 'Numerical' if col in available_num else 'Binary (0/1)',
                'Count': len(df[col].dropna()),
                'Mean': df[col].mean(),
                'Median': df[col].median(),
                'Std_Dev': df[col].std(),
                'Min': df[col].min(),
                'Max': df[col].max()
            })
    
    stats_df = pd.DataFrame(summary_rows)
    
    # =========================================================
    # SECTION 2: CORRELATION WITH SEVERITY
    # =========================================================
    print("\n" + "-" * 50)
    print("2. CORRELATION WITH SEVERITY")
    print("-" * 50)
    
    correlation_rows = []
    if 'Severity' in df.columns:
        for col in all_stat_cols:
            if col != 'Severity' and col in df.columns:
                corr_val = df[col].corr(df['Severity'])
                
                # Interpret correlation strength
                if abs(corr_val) > 0.5:
                    strength = "Strong"
                elif abs(corr_val) > 0.3:
                    strength = "Moderate"
                elif abs(corr_val) > 0.1:
                    strength = "Weak"
                else:
                    strength = "Very Weak / None"
                
                direction = "Positive" if corr_val > 0 else "Negative"
                
                correlation_rows.append({
                    'Feature': col,
                    'Correlation': corr_val,
                    'Strength': strength,
                    'Direction': direction
                })
    
    corr_df = pd.DataFrame(correlation_rows)
    corr_df = corr_df.sort_values('Correlation', key=abs, ascending=False)
    
    # Print top correlations
    print("\n   Top 10 features correlated with severity:")
    for i, row in corr_df.head(10).iterrows():
        print(f"      {row['Feature']}: {row['Correlation']:.4f} ({row['Strength']} {row['Direction']})")
    
    # =========================================================
    # SECTION 3: SEVERITY DISTRIBUTION
    # =========================================================
    print("\n" + "-" * 50)
    print("3. SEVERITY DISTRIBUTION")
    print("-" * 50)
    
    severity_counts = df['Severity'].value_counts().sort_index()
    total = len(df)
    
    severity_rows = []
    for severity in [1, 2, 3, 4]:
        count = severity_counts.get(severity, 0)
        severity_rows.append({
            'Severity_Level': severity,
            'Description': {1: 'Minor', 2: 'Moderate', 3: 'Serious', 4: 'Severe'}[severity],
            'Count': count,
            'Percentage': (count / total) * 100
        })
    
    severity_df = pd.DataFrame(severity_rows)
    
    # =========================================================
    # SECTION 4: CATEGORICAL DISTRIBUTIONS
    # =========================================================
    print("\n" + "-" * 50)
    print("4. CATEGORICAL DISTRIBUTIONS")
    print("-" * 50)
    
    all_categorical_tables = {}
    
    # 4a: State Distribution
    if 'State' in df.columns:
        state_counts = df['State'].value_counts()
        state_rows = []
        for state, count in state_counts.items():
            state_rows.append({
                'State': state,
                'Accidents': count,
                'Percentage': (count / total) * 100,
                'Avg_Severity': df[df['State'] == state]['Severity'].mean()
            })
        all_categorical_tables['State Distribution'] = pd.DataFrame(state_rows)
    
    # 4b: Time of Day Distribution
    if 'TimeOfDay' in df.columns:
        time_order = ['Late Night', 'Morning', 'Afternoon', 'Evening', 'Night']
        time_counts = df['TimeOfDay'].value_counts()
        time_rows = []
        for time in time_order:
            if time in time_counts:
                count = time_counts[time]
                time_rows.append({
                    'Time_Period': time,
                    'Accidents': count,
                    'Percentage': (count / total) * 100,
                    'Avg_Severity': df[df['TimeOfDay'] == time]['Severity'].mean()
                })
        all_categorical_tables['Time of Day Distribution'] = pd.DataFrame(time_rows)
    
    # 4c: Day vs Night
    if 'Sunrise_Sunset' in df.columns:
        dn_counts = df['Sunrise_Sunset'].value_counts()
        dn_rows = []
        for period, count in dn_counts.items():
            dn_rows.append({
                'Period': period,
                'Accidents': count,
                'Percentage': (count / total) * 100,
                'Avg_Severity': df[df['Sunrise_Sunset'] == period]['Severity'].mean()
            })
        all_categorical_tables['Day vs Night'] = pd.DataFrame(dn_rows)
    
    # 4d: Weekend vs Weekday
    if 'IsWeekend' in df.columns:
        weekend_count = df[df['IsWeekend'] == 1].shape[0]
        weekday_count = df[df['IsWeekend'] == 0].shape[0]
        wd_rows = [
            {'Day_Type': 'Weekday', 'Accidents': weekday_count, 'Percentage': (weekday_count / total) * 100},
            {'Day_Type': 'Weekend', 'Accidents': weekend_count, 'Percentage': (weekend_count / total) * 100}
        ]
        all_categorical_tables['Weekend vs Weekday'] = pd.DataFrame(wd_rows)
    
    # 4e: Top 10 Weather Conditions
    if 'Weather_Condition' in df.columns:
        weather_counts = df['Weather_Condition'].value_counts().head(10)
        weather_rows = []
        for weather, count in weather_counts.items():
            weather_rows.append({
                'Weather_Condition': weather,
                'Accidents': count,
                'Percentage': (count / total) * 100,
                'Avg_Severity': df[df['Weather_Condition'] == weather]['Severity'].mean()
            })
        all_categorical_tables['Top 10 Weather Conditions'] = pd.DataFrame(weather_rows)
    
    # =========================================================
    # SECTION 5: GA vs CT COMPARISON
    # =========================================================
    print("\n" + "-" * 50)
    print("5. GA vs CT COMPARISON")
    print("-" * 50)
    
    ga_df = df[df['State'] == 'GA']
    ct_df = df[df['State'] == 'CT']
    
    comparison_rows = [
        {'Metric': 'Total Accidents', 'Georgia': len(ga_df), 'Connecticut': len(ct_df), 'Difference': len(ga_df) - len(ct_df)},
        {'Metric': 'Average Severity', 'Georgia': ga_df['Severity'].mean(), 'Connecticut': ct_df['Severity'].mean(), 'Difference': ga_df['Severity'].mean() - ct_df['Severity'].mean()},
    ]
    
    if 'Temperature(F)' in df.columns:
        comparison_rows.append({'Metric': 'Avg Temperature (°F)', 'Georgia': ga_df['Temperature(F)'].mean(), 'Connecticut': ct_df['Temperature(F)'].mean(), 'Difference': ga_df['Temperature(F)'].mean() - ct_df['Temperature(F)'].mean()})
    
    if 'Humidity(%)' in df.columns:
        comparison_rows.append({'Metric': 'Avg Humidity (%)', 'Georgia': ga_df['Humidity(%)'].mean(), 'Connecticut': ct_df['Humidity(%)'].mean(), 'Difference': ga_df['Humidity(%)'].mean() - ct_df['Humidity(%)'].mean()})
    
    if 'Duration_Minutes' in df.columns:
        comparison_rows.append({'Metric': 'Avg Duration (minutes)', 'Georgia': ga_df['Duration_Minutes'].mean(), 'Connecticut': ct_df['Duration_Minutes'].mean(), 'Difference': ga_df['Duration_Minutes'].mean() - ct_df['Duration_Minutes'].mean()})
    
    comparison_df = pd.DataFrame(comparison_rows)
    
    # =========================================================
    # SECTION 6: SAVE ALL CSV FILES
    # =========================================================
    print("\n" + "-" * 50)
    print("6. SAVING CSV FILES")
    print("-" * 50)
    
    stats_df.to_csv("outputs/statistical_analysis/tables/01_numerical_statistics.csv", index=False)
    corr_df.to_csv("outputs/statistical_analysis/tables/02_correlations.csv", index=False)
    severity_df.to_csv("outputs/statistical_analysis/tables/03_severity_distribution.csv", index=False)
    comparison_df.to_csv("outputs/statistical_analysis/tables/04_ga_vs_ct.csv", index=False)
    
    for name, table in all_categorical_tables.items():
        safe_name = name.lower().replace(' ', '_')
        table.to_csv(f"outputs/statistical_analysis/tables/05_{safe_name}.csv", index=False)
    
    print("   ✅ Saved 10+ CSV files to outputs/statistical_analysis/tables/")
    
    # =========================================================
    # SECTION 7: CREATE EXCEL FILE (All tables in one workbook)
    # =========================================================
    print("\n" + "-" * 50)
    print("7. CREATING EXCEL FILE")
    print("-" * 50)
    
    excel_path = "outputs/statistical_analysis/reports/statistical_analysis.xlsx"
    
    if HAS_OPENPYXL:
        with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
            # Summary sheet
            stats_df.to_excel(writer, sheet_name='Numerical_Stats', index=False)
            corr_df.to_excel(writer, sheet_name='Correlations', index=False)
            severity_df.to_excel(writer, sheet_name='Severity_Distribution', index=False)
            comparison_df.to_excel(writer, sheet_name='GA_vs_CT', index=False)
            
            # Categorical tables
            for name, table in all_categorical_tables.items():
                sheet_name = name.replace(' ', '_')[:31]  # Excel sheet name max 31 chars
                table.to_excel(writer, sheet_name=sheet_name, index=False)
            
            # Add info sheet
            info_df = pd.DataFrame({
                'Information': ['Analysis Date', 'Total Accidents', 'Date Range'],
                'Value': [datetime.now().strftime('%Y-%m-%d %H:%M:%S'), len(df), 
                          f"{df['Start_Time'].min().date()} to {df['Start_Time'].max().date()}" if 'Start_Time' in df.columns else 'N/A']
            })
            info_df.to_excel(writer, sheet_name='Info', index=False)
        
        print(f"   ✅ Excel file saved: {excel_path}")
    else:
        print("   ⚠️ openpyxl not installed. Skipping Excel export.")
    
    # =========================================================
    # SECTION 8: CREATE WORD REPORT
    # =========================================================
    print("\n" + "-" * 50)
    print("8. CREATING WORD REPORT")
    print("-" * 50)
    
    word_path = "outputs/statistical_analysis/reports/statistical_analysis.docx"
    
    if HAS_PYTHON_DOCX:
        doc = Document()
        
        # Title
        title = doc.add_heading('US Accidents Statistical Analysis Report', 0)
        title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # Info
        doc.add_paragraph(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        doc.add_paragraph(f"Total Accidents Analyzed: {len(df):,}")
        if 'Start_Time' in df.columns:
            doc.add_paragraph(f"Date Range: {df['Start_Time'].min().date()} to {df['Start_Time'].max().date()}")
        doc.add_paragraph(f"States: Georgia (GA) and Connecticut (CT)")
        doc.add_paragraph()
        
        # 1. Severity Distribution
        doc.add_heading('1. Accident Severity Distribution', level=1)
        table = doc.add_table(rows=1, cols=3)
        table.style = 'Table Grid'
        hdr = table.rows[0].cells
        hdr[0].text = 'Severity Level'
        hdr[1].text = 'Description'
        hdr[2].text = 'Count'
        for _, row in severity_df.iterrows():
            cells = table.add_row().cells
            cells[0].text = str(int(row['Severity_Level']))
            cells[1].text = row['Description']
            cells[2].text = f"{int(row['Count']):,}"
        doc.add_paragraph()
        
        # 2. Key Findings from Correlations
        doc.add_heading('2. Key Factors Correlated with Severity', level=1)
        doc.add_paragraph("The following features show the strongest correlation with accident severity:")
        
        table = doc.add_table(rows=1, cols=3)
        table.style = 'Table Grid'
        hdr = table.rows[0].cells
        hdr[0].text = 'Feature'
        hdr[1].text = 'Correlation'
        hdr[2].text = 'Strength'
        for _, row in corr_df.head(10).iterrows():
            cells = table.add_row().cells
            cells[0].text = row['Feature']
            cells[1].text = f"{row['Correlation']:.4f}"
            cells[2].text = row['Strength']
        doc.add_paragraph()
        
        # 3. GA vs CT Comparison
        doc.add_heading('3. Georgia vs Connecticut Comparison', level=1)
        table = doc.add_table(rows=1, cols=4)
        table.style = 'Table Grid'
        hdr = table.rows[0].cells
        hdr[0].text = 'Metric'
        hdr[1].text = 'Georgia'
        hdr[2].text = 'Connecticut'
        hdr[3].text = 'Difference'
        for _, row in comparison_df.iterrows():
            cells = table.add_row().cells
            cells[0].text = row['Metric']
            cells[1].text = f"{row['Georgia']:.1f}" if isinstance(row['Georgia'], float) else f"{row['Georgia']:,}"
            cells[2].text = f"{row['Connecticut']:.1f}" if isinstance(row['Connecticut'], float) else f"{row['Connecticut']:,}"
            cells[3].text = f"{row['Difference']:.1f}" if isinstance(row['Difference'], float) else f"{row['Difference']:,}"
        doc.add_paragraph()
        
        # 4. Time Patterns
        if 'Time of Day Distribution' in all_categorical_tables:
            doc.add_heading('4. Accident Patterns by Time of Day', level=1)
            time_table = all_categorical_tables['Time of Day Distribution']
            table = doc.add_table(rows=1, cols=4)
            table.style = 'Table Grid'
            hdr = table.rows[0].cells
            hdr[0].text = 'Time Period'
            hdr[1].text = 'Accidents'
            hdr[2].text = 'Percentage'
            hdr[3].text = 'Avg Severity'
            for _, row in time_table.iterrows():
                cells = table.add_row().cells
                cells[0].text = row['Time_Period']
                cells[1].text = f"{int(row['Accidents']):,}"
                cells[2].text = f"{row['Percentage']:.1f}%"
                cells[3].text = f"{row['Avg_Severity']:.2f}"
        
        # Save Word document
        doc.save(word_path)
        print(f"   ✅ Word report saved: {word_path}")
    else:
        print("   ⚠️ python-docx not installed. Skipping Word export.")
    
    # =========================================================
    # FINAL SUMMARY
    # =========================================================
    print("\n" + "=" * 70)
    print("📊 STATISTICAL ANALYSIS - SUMMARY")
    print("=" * 70)
    
    # Key insights
    print(f"""
✅ ANALYSIS COMPLETE!

KEY INSIGHTS:
------------
• Total Accidents: {len(df):,}
• Average Severity: {df['Severity'].mean():.2f} (1=Minor, 4=Severe)
• Most Common Severity: {df['Severity'].mode()[0]}

TOP CORRELATIONS WITH SEVERITY:
""")
    for _, row in corr_df.head(5).iterrows():
        print(f"   • {row['Feature']}: {row['Correlation']:.4f} ({row['Strength']})")

    print(f"""
OUTPUT FILES:
------------
📁 CSV Files: outputs/statistical_analysis/tables/
   ├── 01_numerical_statistics.csv
   ├── 02_correlations.csv
   ├── 03_severity_distribution.csv
   ├── 04_ga_vs_ct.csv
   └── 05_*.csv (categorical tables)

📊 Excel File: outputs/statistical_analysis/reports/statistical_analysis.xlsx
   (All tables in one workbook)

📄 Word Report: outputs/statistical_analysis/reports/statistical_analysis.docx
   (Professional report with formatted tables)
""")
    
    print("=" * 70)
    print("✨ STATISTICAL ANALYSIS COMPLETE! ✨")
    print("=" * 70)
    
    return df

if __name__ == "__main__" or __name__ == "statistical_analysis":
    run_statistical_analysis()