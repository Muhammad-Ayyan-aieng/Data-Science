# advanced_features_analysis.py
"""
Advanced Analysis of Road Features, Geography, and Risk Factors
Includes: road features, geographic patterns, risk combinations, seasonal analysis
Exports to: 1 Excel file, 1 Word file, multiple CSV files
"""

import pandas as pd
import numpy as np
import os
from scipy import stats
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Optional imports for Excel and Word
try:
    from openpyxl import Workbook
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

def analyze_all_features():
    """Complete analysis of road features, geography, and risk combinations"""
    
    print("=" * 80)
    print("🔍 ADVANCED FEATURES ANALYSIS - ROAD SAFETY & RISK FACTORS")
    print("=" * 80)
    
    # Create output folders
    os.makedirs("outputs/advanced_features/tables", exist_ok=True)
    os.makedirs("outputs/advanced_features/reports", exist_ok=True)
    
    # Load data
    input_file = os.path.join("datasets", "cleaned_accidents.csv")
    df = pd.read_csv(input_file)
    print(f"\n✅ Loaded {len(df):,} accidents")
    print(f"✅ Columns: {len(df.columns)}")
    
    # Dictionary to store all tables for Excel export
    all_tables = {}
    
    # =========================================================
    # 1. ROAD FEATURES IMPACT (Skip low-frequency features)
    # =========================================================
    print("\n" + "-" * 50)
    print("1. ROAD FEATURES IMPACT ON SEVERITY")
    print("-" * 50)
    
    road_features = [
        ('Traffic_Calming', 'Speed bumps, raised crosswalks'),
        ('No_Exit', 'Dead end street'),
        ('Station', 'Train/bus station nearby'),
        ('Amenity', 'Restaurants, cafes nearby'),
        ('Traffic_Signal', 'Traffic light'),
        ('Crossing', 'Pedestrian crosswalk'),
        ('Junction', 'Intersection'),
        ('Stop', 'Stop sign'),
        ('Railway', 'Railroad crossing')
    ]
    
    road_results = []
    for feature, description in road_features:
        if feature in df.columns:
            true_mask = df[feature] == True
            true_count = true_mask.sum()
            
            # Skip features with less than 50 occurrences
            if true_count < 50:
                print(f"\n{feature}: Skipped (only {true_count} occurrences, need >50)")
                continue
            
            true_severity = df[true_mask]['Severity'].mean()
            false_severity = df[df[feature] == False]['Severity'].mean()
            diff = true_severity - false_severity
            
            # T-test for significance
            t_stat, p_value = stats.ttest_ind(
                df[true_mask]['Severity'], 
                df[df[feature] == False]['Severity']
            )
            
            road_results.append({
                'Road_Feature': description,
                'Present_Count': int(true_count),
                'Present_Percentage': (true_count / len(df)) * 100,
                'Severity_With': true_severity,
                'Severity_Without': false_severity,
                'Difference': diff,
                'P_Value': p_value,
                'Statistically_Significant': p_value < 0.05
            })
            
            # Print with formatted percentages
            print(f"\n{feature} ({description}):")
            print(f"   Present in {true_count:,} accidents ({true_count/len(df)*100:.1f}%)")
            print(f"   Severity with feature: {true_severity:.3f}")
            print(f"   Severity without feature: {false_severity:.3f}")
            print(f"   Difference: {diff:+.3f} ({diff*100:+.1f}%)")
            print(f"   Statistically significant: {'✅' if p_value < 0.05 else '❌'} (p={p_value:.4f})")
    
    road_df = pd.DataFrame(road_results)
    road_df = road_df.sort_values('Difference', ascending=True)
    all_tables['Road Features Impact'] = road_df
    
    # =========================================================
    # 2. SEASONAL ANALYSIS (NEW!)
    # =========================================================
    print("\n" + "-" * 50)
    print("2. SEASONAL ANALYSIS")
    print("-" * 50)
    
    def get_season(month):
        if month in [3, 4, 5]:
            return 'Spring'
        elif month in [6, 7, 8]:
            return 'Summer'
        elif month in [9, 10, 11]:
            return 'Fall'
        else:
            return 'Winter'
    
    if 'Month' in df.columns:
        df['Season'] = df['Month'].apply(get_season)
        season_stats = df.groupby('Season')['Severity'].agg(['mean', 'count', 'std']).reset_index()
        season_stats.columns = ['Season', 'Avg_Severity', 'Accident_Count', 'Std_Dev']
        season_stats = season_stats.sort_values('Avg_Severity', ascending=False)
        
        print("\n📊 Severity by Season:")
        print(season_stats.to_string(index=False))
        all_tables['Seasonal Analysis'] = season_stats
    
    # =========================================================
    # 3. HIGHWAY vs LOCAL ROAD ANALYSIS (NEW!)
    # =========================================================
    print("\n" + "-" * 50)
    print("3. HIGHWAY vs LOCAL ROAD ANALYSIS")
    print("-" * 50)
    
    if 'Street' in df.columns:
        df['Is_Highway'] = df['Street'].str.contains('I-|US-|STATE-|SR-', case=False, na=False).astype(int)
        
        highway_stats = df.groupby('Is_Highway')['Severity'].agg(['mean', 'count', 'std']).reset_index()
        highway_stats['Road_Type'] = highway_stats['Is_Highway'].map({1: 'Highway', 0: 'Local Road'})
        
        # T-test between highway and local roads
        highway_sev = df[df['Is_Highway'] == 1]['Severity']
        local_sev = df[df['Is_Highway'] == 0]['Severity']
        t_stat, p_value = stats.ttest_ind(highway_sev, local_sev)
        
        print(f"\n📊 Highway vs Local Road Comparison:")
        print(f"   Highway accidents: {highway_sev.count():,} (Severity: {highway_sev.mean():.3f})")
        print(f"   Local road accidents: {local_sev.count():,} (Severity: {local_sev.mean():.3f})")
        print(f"   Difference: {highway_sev.mean() - local_sev.mean():+.3f}")
        print(f"   Statistically significant: {'✅' if p_value < 0.05 else '❌'} (p={p_value:.4f})")
        
        highway_result = pd.DataFrame([{
            'Road_Type': 'Highway',
            'Accident_Count': int(highway_sev.count()),
            'Avg_Severity': highway_sev.mean(),
            'Std_Dev': highway_sev.std()
        }, {
            'Road_Type': 'Local Road',
            'Accident_Count': int(local_sev.count()),
            'Avg_Severity': local_sev.mean(),
            'Std_Dev': local_sev.std()
        }])
        all_tables['Highway vs Local'] = highway_result
    
    # =========================================================
    # 4. TEXT + ROAD COMBINATIONS (NEW!)
    # =========================================================
    print("\n" + "-" * 50)
    print("4. TEXT + ROAD FEATURE COMBINATIONS")
    print("-" * 50)
    
    text_road_combos = [
        ('has_blocked + Junction', 
         (df['has_blocked'] == 1) & (df['Junction'] == True),
         'Blocks + Intersection'),
        ('has_blocked + No Signal', 
         (df['has_blocked'] == 1) & (df['Traffic_Signal'] == False),
         'Blocks + No Traffic Light'),
        ('has_jackknife + Highway', 
         (df['has_jackknife'] == 1) & (df['Is_Highway'] == 1) if 'Is_Highway' in df.columns else None,
         'Truck Accident on Highway'),
        ('has_road_closed + Night', 
         (df['has_road_closed'] == 1) & (df['Sunrise_Sunset'] == 'Night'),
         'Road Closed at Night'),
        ('has_multi_vehicle + Junction', 
         (df['has_multi_vehicle'] == 1) & (df['Junction'] == True),
         'Multi-Vehicle at Intersection'),
        ('has_slow_traffic + Rush_Hour', 
         (df['has_slow_traffic'] == 1) & (df.get('Rush_Hour', pd.Series(0)) == 1),
         'Slow Traffic During Rush Hour')
    ]
    
    baseline_avg = df['Severity'].mean()
    text_road_results = []
    
    print("\n📊 Text + Road Combinations Impact:")
    for name, condition, description in text_road_combos:
        if condition is not None:
            count = condition.sum()
            if count > 50:
                avg_sev = df[condition]['Severity'].mean()
                diff = avg_sev - baseline_avg
                text_road_results.append({
                    'Combination': description,
                    'Accident_Count': int(count),
                    'Percentage': (count / len(df)) * 100,
                    'Avg_Severity': avg_sev,
                    'Difference_from_Baseline': diff
                })
                print(f"\n   {description}:")
                print(f"      Accidents: {count:,} ({count/len(df)*100:.1f}%)")
                print(f"      Avg Severity: {avg_sev:.3f} (baseline: {baseline_avg:.3f})")
                print(f"      Difference: {diff:+.3f}")
    
    if text_road_results:
        text_road_df = pd.DataFrame(text_road_results)
        text_road_df = text_road_df.sort_values('Difference_from_Baseline', ascending=False)
        all_tables['Text + Road Combinations'] = text_road_df
    
    # =========================================================
    # 5. GEOGRAPHIC ANALYSIS - CITIES
    # =========================================================
    print("\n" + "-" * 50)
    print("5. GEOGRAPHIC ANALYSIS - CITIES")
    print("-" * 50)
    
    city_stats = df.groupby('City')['Severity'].agg(['mean', 'count']).reset_index()
    city_stats.columns = ['City', 'Avg_Severity', 'Accident_Count']
    city_stats = city_stats[city_stats['Accident_Count'] >= 100].sort_values('Avg_Severity', ascending=False)
    
    # Add severe percentage
    severe_pct = []
    for city in city_stats['City']:
        city_df = df[df['City'] == city]
        severe_count = city_df[city_df['Severity'] >= 3].shape[0]
        severe_pct.append((severe_count / len(city_df)) * 100)
    city_stats['Severe_Accidents_Pct'] = severe_pct
    
    dangerous_cities = city_stats.head(10).copy()
    safest_cities = city_stats.tail(10).copy()
    
    print("\n📊 TOP 10 MOST DANGEROUS CITIES:")
    print(dangerous_cities.to_string(index=False))
    print("\n📊 TOP 10 SAFEST CITIES:")
    print(safest_cities.to_string(index=False))
    
    all_tables['Most Dangerous Cities'] = dangerous_cities
    all_tables['Safest Cities'] = safest_cities
    
    # =========================================================
    # 6. MULTIPLE RISK FACTOR COMBINATIONS
    # =========================================================
    print("\n" + "-" * 50)
    print("6. MULTIPLE RISK FACTOR COMBINATIONS")
    print("-" * 50)
    
    combinations = [
        ('Junction + No Traffic Signal + Crossing', 
         (df['Junction'] == True) & (df['Traffic_Signal'] == False) & (df['Crossing'] == True)),
        ('Junction + Traffic Signal',
         (df['Junction'] == True) & (df['Traffic_Signal'] == True)),
        ('Railway Crossing + No Signal',
         (df['Railway'] == True) & (df['Traffic_Signal'] == False)),
        ('School Zone (Amenity + Crossing)',
         (df['Amenity'] == True) & (df['Crossing'] == True)),
        ('High Risk Intersection (Junction + Crossing + No Roundabout)',
         (df['Junction'] == True) & (df['Crossing'] == True) & (df['Roundabout'] == False)),
        ('Low Risk Setup (Roundabout + No Junction + No Crossing)',
         (df['Roundabout'] == True) & (df['Junction'] == False) & (df['Crossing'] == False))
    ]
    
    baseline_avg = df['Severity'].mean()
    baseline_severe = (df['Severity'] >= 3).sum() / len(df) * 100
    
    combo_results = []
    for name, condition in combinations:
        count = condition.sum()
        if count > 50:
            avg_sev = df[condition]['Severity'].mean()
            severe_pct_val = (df[condition]['Severity'] >= 3).sum() / count * 100
            
            combo_results.append({
                'Situation': name,
                'Accident_Count': int(count),
                'Percentage_of_Total': (count / len(df)) * 100,
                'Avg_Severity': avg_sev,
                'Severe_Accidents_Pct': severe_pct_val,
                'vs_Baseline_Avg': avg_sev - baseline_avg,
                'vs_Baseline_Severe': severe_pct_val - baseline_severe
            })
    
    combo_df = pd.DataFrame(combo_results)
    combo_df = combo_df.sort_values('Avg_Severity', ascending=False)
    all_tables['Risk Combinations'] = combo_df
    
    # =========================================================
    # 7. GA vs CT ROAD FEATURE COMPARISON
    # =========================================================
    print("\n" + "-" * 50)
    print("7. GA vs CT ROAD FEATURE COMPARISON")
    print("-" * 50)
    
    ga_df = df[df['State'] == 'GA']
    ct_df = df[df['State'] == 'CT']
    
    ga_ct_results = []
    for feature, description in road_features:
        if feature in df.columns and feature != 'Bump' and feature != 'Turning_Loop':
            ga_pct = (ga_df[feature].sum() / len(ga_df)) * 100
            ct_pct = (ct_df[feature].sum() / len(ct_df)) * 100
            ga_ct_results.append({
                'Road_Feature': description,
                'Georgia_Pct': ga_pct,
                'Connecticut_Pct': ct_pct,
                'Difference': ga_pct - ct_pct
            })
    
    ga_ct_df = pd.DataFrame(ga_ct_results)
    all_tables['GA vs CT Road Features'] = ga_ct_df
    
    # =========================================================
    # 8. SAVE CSV FILES
    # =========================================================
    print("\n" + "-" * 50)
    print("8. SAVING CSV FILES")
    print("-" * 50)
    
    road_df.to_csv("outputs/advanced_features/tables/01_road_features_impact.csv", index=False)
    if 'Seasonal Analysis' in all_tables:
        all_tables['Seasonal Analysis'].to_csv("outputs/advanced_features/tables/02_seasonal_analysis.csv", index=False)
    if 'Highway vs Local' in all_tables:
        all_tables['Highway vs Local'].to_csv("outputs/advanced_features/tables/03_highway_vs_local.csv", index=False)
    if 'Text + Road Combinations' in all_tables:
        all_tables['Text + Road Combinations'].to_csv("outputs/advanced_features/tables/04_text_road_combinations.csv", index=False)
    dangerous_cities.to_csv("outputs/advanced_features/tables/05_dangerous_cities.csv", index=False)
    safest_cities.to_csv("outputs/advanced_features/tables/06_safest_cities.csv", index=False)
    combo_df.to_csv("outputs/advanced_features/tables/07_risk_combinations.csv", index=False)
    ga_ct_df.to_csv("outputs/advanced_features/tables/08_ga_ct_road_features.csv", index=False)
    
    print("   ✅ Saved 8 CSV files to outputs/advanced_features/tables/")
    
    # =========================================================
    # 9. CREATE EXCEL FILE
    # =========================================================
    print("\n" + "-" * 50)
    print("9. CREATING EXCEL FILE")
    print("-" * 50)
    
    excel_path = "outputs/advanced_features/reports/advanced_features_analysis.xlsx"
    
    if HAS_OPENPYXL:
        with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
            for sheet_name, table in all_tables.items():
                safe_name = sheet_name.replace(' ', '_')[:31]
                table.to_excel(writer, sheet_name=safe_name, index=False)
            
            # Add info sheet
            info_df = pd.DataFrame({
                'Information': ['Analysis Date', 'Total Accidents', 'States Analyzed'],
                'Value': [datetime.now().strftime('%Y-%m-%d %H:%M:%S'), len(df), 'Georgia (GA) and Connecticut (CT)']
            })
            info_df.to_excel(writer, sheet_name='Info', index=False)
        
        print(f"   ✅ Excel file saved: {excel_path}")
    else:
        print("   ⚠️ openpyxl not installed. Skipping Excel export.")
    
    # =========================================================
    # 10. CREATE WORD REPORT
    # =========================================================
    print("\n" + "-" * 50)
    print("10. CREATING WORD REPORT")
    print("-" * 50)
    
    word_path = "outputs/advanced_features/reports/advanced_features_analysis.docx"
    
    if HAS_PYTHON_DOCX:
        doc = Document()
        
        # Title
        title = doc.add_heading('Advanced Features Analysis Report', 0)
        title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # Info
        doc.add_paragraph(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        doc.add_paragraph(f"Total Accidents Analyzed: {len(df):,}")
        doc.add_paragraph()
        
        # 1. Key Findings Summary
        doc.add_heading('1. Key Findings Summary', level=1)
        
        # Most dangerous feature
        if len(road_results) > 0:
            most_dangerous = max(road_results, key=lambda x: x['Difference'])
            safest = min(road_results, key=lambda x: x['Difference'])
            doc.add_paragraph(f"• MOST DANGEROUS: {most_dangerous['Road_Feature']} "
                            f"(+{most_dangerous['Difference']:.3f} severity)")
            doc.add_paragraph(f"• SAFEST: {safest['Road_Feature']} "
                            f"({safest['Difference']:.3f} severity)")
        
        # 2. Road Features Impact
        doc.add_heading('2. Road Features Impact on Severity', level=1)
        table = doc.add_table(rows=1, cols=4)
        table.style = 'Table Grid'
        hdr = table.rows[0].cells
        hdr[0].text = 'Road Feature'
        hdr[1].text = 'Severity With'
        hdr[2].text = 'Severity Without'
        hdr[3].text = 'Difference'
        
        for _, row in road_df.head(10).iterrows():
            cells = table.add_row().cells
            cells[0].text = row['Road_Feature']
            cells[1].text = f"{row['Severity_With']:.2f}"
            cells[2].text = f"{row['Severity_Without']:.2f}"
            cells[3].text = f"{row['Difference']:+.3f}"
        
        doc.add_paragraph()
        
        # 3. Most Dangerous Cities
        doc.add_heading('3. Top 5 Most Dangerous Cities', level=1)
        table = doc.add_table(rows=1, cols=3)
        table.style = 'Table Grid'
        hdr = table.rows[0].cells
        hdr[0].text = 'City'
        hdr[1].text = 'Avg Severity'
        hdr[2].text = 'Severe %'
        
        for _, row in dangerous_cities.head(5).iterrows():
            cells = table.add_row().cells
            cells[0].text = row['City']
            cells[1].text = f"{row['Avg_Severity']:.2f}"
            cells[2].text = f"{row['Severe_Accidents_Pct']:.1f}%"
        
        doc.add_paragraph()
        
        # 4. Safest Cities
        doc.add_heading('4. Top 5 Safest Cities', level=1)
        table = doc.add_table(rows=1, cols=3)
        table.style = 'Table Grid'
        hdr = table.rows[0].cells
        hdr[0].text = 'City'
        hdr[1].text = 'Avg Severity'
        hdr[2].text = 'Severe %'
        
        for _, row in safest_cities.head(5).iterrows():
            cells = table.add_row().cells
            cells[0].text = row['City']
            cells[1].text = f"{row['Avg_Severity']:.2f}"
            cells[2].text = f"{row['Severe_Accidents_Pct']:.1f}%"
        
        doc.add_paragraph()
        
        # 5. Seasonal Analysis
        if 'Seasonal Analysis' in all_tables:
            doc.add_heading('5. Seasonal Analysis', level=1)
            season_data = all_tables['Seasonal Analysis']
            table = doc.add_table(rows=1, cols=3)
            table.style = 'Table Grid'
            hdr = table.rows[0].cells
            hdr[0].text = 'Season'
            hdr[1].text = 'Avg Severity'
            hdr[2].text = 'Accidents'
            
            for _, row in season_data.iterrows():
                cells = table.add_row().cells
                cells[0].text = row['Season']
                cells[1].text = f"{row['Avg_Severity']:.2f}"
                cells[2].text = f"{int(row['Accident_Count']):,}"
        
        # Save Word document
        doc.save(word_path)
        print(f"   ✅ Word report saved: {word_path}")
    else:
        print("   ⚠️ python-docx not installed. Skipping Word export.")
    
    # =========================================================
    # 11. FINAL SUMMARY
    # =========================================================
    print("\n" + "=" * 80)
    print("📊 ADVANCED FEATURES ANALYSIS - SUMMARY")
    print("=" * 80)
    
    # Find best and worst features
    if len(road_results) > 0:
        most_dangerous = max(road_results, key=lambda x: x['Difference'])
        safest = min(road_results, key=lambda x: x['Difference'])
        
        print(f"""
✅ ANALYSIS COMPLETE!

KEY FINDINGS:
------------
🔴 MOST DANGEROUS ROAD FEATURE:
   • {most_dangerous['Road_Feature']}: +{most_dangerous['Difference']:.3f} severity
   • Present in {most_dangerous['Present_Count']:,} accidents ({most_dangerous['Present_Percentage']:.1f}%)

🟢 SAFEST ROAD FEATURE:
   • {safest['Road_Feature']}: {safest['Difference']:.3f} severity
   • Present in {safest['Present_Count']:,} accidents ({safest['Present_Percentage']:.1f}%)

📍 MOST DANGEROUS CITY:
   • {dangerous_cities.iloc[0]['City']}: Severity {dangerous_cities.iloc[0]['Avg_Severity']:.2f}

📍 SAFEST CITY:
   • {safest_cities.iloc[0]['City']}: Severity {safest_cities.iloc[0]['Avg_Severity']:.2f}

OUTPUT FILES:
------------
📁 CSV Files: outputs/advanced_features/tables/ (8 files)
📊 Excel File: outputs/advanced_features/reports/advanced_features_analysis.xlsx
📄 Word Report: outputs/advanced_features/reports/advanced_features_analysis.docx
""")
    
    print("=" * 80)
    print("✨ ADVANCED FEATURES ANALYSIS COMPLETE! ✨")
    print("=" * 80)
    
    return all_tables

if __name__ == "__main__" or __name__ == "advanced_features_analysis":
    analyze_all_features()