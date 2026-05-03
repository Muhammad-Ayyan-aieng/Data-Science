# visualization.py
"""
Step 7: Create Professional Visualizations from All Analysis Results
Generates essential charts for report using CSV outputs from all analysis modules
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np

# Set professional style for all plots
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("Set2")
sns.set_context("talk", font_scale=1.2)

# Create output folder for figures
os.makedirs("outputs/figures", exist_ok=True)

print("=" * 80)
print("🎨 VISUALIZATION - CREATING CHARTS FOR REPORT")
print("=" * 80)

# Helper function to safely read CSV
def safe_read_csv(filepath, **kwargs):
    try:
        return pd.read_csv(filepath, **kwargs)
    except FileNotFoundError:
        print(f"   ⚠️ File not found: {filepath}")
        return None

# =========================================================
# CHART 1: SEVERITY DISTRIBUTION
# =========================================================
print("\n📊 Creating Chart 1: Severity Distribution...")

severity_df = safe_read_csv("outputs/statistical_analysis/tables/03_severity_distribution.csv")

if severity_df is not None:
    plt.figure(figsize=(10, 6))
    colors = ['#2ecc71', '#f39c12', '#e74c3c', '#c0392b']
    
    # Handle column names
    if 'Severity_Level' in severity_df.columns:
        x_vals = severity_df['Severity_Level']
        y_vals = severity_df['Count']
    else:
        x_vals = severity_df.iloc[:, 0]
        y_vals = severity_df.iloc[:, 1]
    
    bars = plt.bar(x_vals.astype(str), y_vals, color=colors, edgecolor='black')
    plt.xlabel('Severity Level', fontsize=14)
    plt.ylabel('Number of Accidents', fontsize=14)
    plt.title('Accident Severity Distribution (GA & CT)', fontsize=16, fontweight='bold')

    for bar, count in zip(bars, y_vals):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5000, 
                 f'{int(count):,}', ha='center', va='bottom', fontsize=11)

    plt.tight_layout()
    plt.savefig("outputs/figures/01_severity_distribution.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("   ✅ Saved: 01_severity_distribution.png")

# =========================================================
# CHART 2: TIME OF DAY DISTRIBUTION (FIXED PATH)
# =========================================================
print("\n📊 Creating Chart 2: Time of Day Distribution...")

time_df = safe_read_csv("outputs/statistical_analysis/tables/05_time_of_day_distribution.csv")

if time_df is not None:
    plt.figure(figsize=(12, 6))
    colors_bar = ['#34495e', '#e74c3c', '#f39c12', '#2ecc71', '#3498db']
    
    # Handle column names
    if 'Time_Period' in time_df.columns:
        x_vals = time_df['Time_Period']
        y_vals = time_df['Accidents']
    else:
        x_vals = time_df.iloc[:, 0]
        y_vals = time_df.iloc[:, 1]
    
    bars = plt.bar(x_vals, y_vals, color=colors_bar, edgecolor='black')
    plt.xlabel('Time of Day', fontsize=14)
    plt.ylabel('Number of Accidents', fontsize=14)
    plt.title('Accident Distribution by Time of Day', fontsize=16, fontweight='bold')

    for bar, count in zip(bars, y_vals):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2000, 
                 f'{int(count):,}', ha='center', va='bottom', fontsize=10)

    plt.tight_layout()
    plt.savefig("outputs/figures/02_time_of_day_distribution.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("   ✅ Saved: 02_time_of_day_distribution.png")
else:
    print("   ❌ Skipped: time_of_day_distribution.csv not found")

# =========================================================
# CHART 3: GA vs CT SEVERITY COMPARISON
# =========================================================
print("\n📊 Creating Chart 3: GA vs CT Severity Comparison...")

ga_ct_df = safe_read_csv("outputs/comparison_analysis/tables/01_significance.csv")

if ga_ct_df is not None:
    plt.figure(figsize=(8, 6))
    states = ['Georgia', 'Connecticut']
    severities = [ga_ct_df['Georgia_Mean'].iloc[0], ga_ct_df['Connecticut_Mean'].iloc[0]]
    colors_state = ['#3498db', '#2ecc71']
    bars = plt.bar(states, severities, color=colors_state, edgecolor='black')
    plt.xlabel('State', fontsize=14)
    plt.ylabel('Average Severity', fontsize=14)
    plt.title('Average Accident Severity: Georgia vs Connecticut', fontsize=16, fontweight='bold')
    plt.ylim(0, 4)

    for bar, severity in zip(bars, severities):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05, 
                 f'{severity:.2f}', ha='center', va='bottom', fontsize=12)

    plt.tight_layout()
    plt.savefig("outputs/figures/03_ga_vs_ct_severity.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("   ✅ Saved: 03_ga_vs_ct_severity.png")

# =========================================================
# CHART 4: KEYWORD SEVERITY IMPACT
# =========================================================
print("\n📊 Creating Chart 4: Keyword Severity Impact...")

keyword_df = safe_read_csv("outputs/text_analysis/tables/02_keyword_impact.csv")

if keyword_df is not None:
    keyword_df = keyword_df.sort_values('Avg_Severity', ascending=False)

    plt.figure(figsize=(12, 8))
    colors_keyword = ['#c0392b' if x > 2.6 else '#e74c3c' if x > 2.4 else '#f39c12' if x > 2.2 else '#2ecc71' 
                      for x in keyword_df['Avg_Severity']]
    bars = plt.barh(keyword_df['Keyword'], keyword_df['Avg_Severity'], 
                    color=colors_keyword, edgecolor='black')
    plt.xlabel('Average Severity', fontsize=14)
    plt.ylabel('Keyword', fontsize=14)
    plt.title('Impact of Keywords on Accident Severity', fontsize=16, fontweight='bold')
    plt.xlim(2.0, 3.2)
    plt.axvline(x=2.46, color='gray', linestyle='--', label='Overall Average (2.46)')
    plt.legend()

    for bar, severity in zip(bars, keyword_df['Avg_Severity']):
        plt.text(bar.get_width() + 0.02, bar.get_y() + bar.get_height()/2, 
                 f'{severity:.2f}', ha='left', va='center', fontsize=10)

    plt.tight_layout()
    plt.savefig("outputs/figures/04_keyword_severity_impact.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("   ✅ Saved: 04_keyword_severity_impact.png")

# =========================================================
# CHART 5: ROAD FEATURES IMPACT
# =========================================================
print("\n📊 Creating Chart 5: Road Features Impact...")

road_df = safe_read_csv("outputs/advanced_features/tables/01_road_features_impact.csv")

if road_df is not None:
    road_df = road_df.sort_values('Difference', ascending=True)

    plt.figure(figsize=(12, 8))
    colors_road = ['#2ecc71' if x < 0 else '#e74c3c' for x in road_df['Difference']]
    bars = plt.barh(road_df['Road_Feature'], road_df['Difference'], 
                    color=colors_road, edgecolor='black')
    plt.xlabel('Difference in Severity (Present - Absent)', fontsize=14)
    plt.ylabel('Road Feature', fontsize=14)
    plt.title('Impact of Road Features on Accident Severity', fontsize=16, fontweight='bold')
    plt.axvline(x=0, color='black', linestyle='-', linewidth=1)

    for bar, diff in zip(bars, road_df['Difference']):
        plt.text(bar.get_width() + 0.01 if diff > 0 else bar.get_width() - 0.08, 
                 bar.get_y() + bar.get_height()/2, 
                 f'{diff:+.2f}', ha='left' if diff > 0 else 'right', va='center', fontsize=10)

    plt.tight_layout()
    plt.savefig("outputs/figures/05_road_features_impact.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("   ✅ Saved: 05_road_features_impact.png")

# =========================================================
# CHART 6: MOST DANGEROUS CITIES
# =========================================================
print("\n📊 Creating Chart 6: Most Dangerous Cities...")

city_df = safe_read_csv("outputs/advanced_features/tables/05_dangerous_cities.csv")

if city_df is not None:
    plt.figure(figsize=(12, 8))
    bars = plt.barh(city_df['City'], city_df['Avg_Severity'], 
                    color='#e74c3c', edgecolor='black')
    plt.xlabel('Average Severity', fontsize=14)
    plt.ylabel('City', fontsize=14)
    plt.title('Top 10 Most Dangerous Cities', fontsize=16, fontweight='bold')
    plt.xlim(2.5, 3.2)
    plt.gca().invert_yaxis()

    for bar, severity in zip(bars, city_df['Avg_Severity']):
        plt.text(bar.get_width() + 0.02, bar.get_y() + bar.get_height()/2, 
                 f'{severity:.2f}', ha='left', va='center', fontsize=10)

    plt.tight_layout()
    plt.savefig("outputs/figures/06_most_dangerous_cities.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("   ✅ Saved: 06_most_dangerous_cities.png")

# =========================================================
# CHART 7: RISK COMBINATIONS
# =========================================================
print("\n📊 Creating Chart 7: Risk Combinations...")

risk_df = safe_read_csv("outputs/advanced_features/tables/07_risk_combinations.csv")

if risk_df is not None:
    plt.figure(figsize=(12, 8))
    colors_risk = ['#e74c3c' if x > 2.6 else '#f39c12' if x > 2.5 else '#2ecc71' 
                   for x in risk_df['Avg_Severity']]
    bars = plt.barh(risk_df['Situation'], risk_df['Avg_Severity'], 
                    color=colors_risk, edgecolor='black')
    plt.xlabel('Average Severity', fontsize=14)
    plt.ylabel('Risk Combination', fontsize=14)
    plt.title('Accident Severity by Risk Factor Combinations', fontsize=16, fontweight='bold')
    plt.axvline(x=2.46, color='gray', linestyle='--', label='Overall Average (2.46)')
    plt.legend()
    plt.gca().invert_yaxis()

    for bar, severity in zip(bars, risk_df['Avg_Severity']):
        plt.text(bar.get_width() + 0.02, bar.get_y() + bar.get_height()/2, 
                 f'{severity:.2f}', ha='left', va='center', fontsize=9)

    plt.tight_layout()
    plt.savefig("outputs/figures/07_risk_combinations.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("   ✅ Saved: 07_risk_combinations.png")

# =========================================================
# CHART 8: WEEKEND vs WEEKDAY (FIXED PATH)
# =========================================================
print("\n📊 Creating Chart 8: Weekend vs Weekday...")

weekend_df = safe_read_csv("outputs/statistical_analysis/tables/05_weekend_vs_weekday.csv")

if weekend_df is not None:
    plt.figure(figsize=(8, 6))
    colors_wk = ['#f39c12', '#3498db']
    
    # Handle column names
    if 'Day_Type' in weekend_df.columns:
        x_vals = weekend_df['Day_Type']
        y_vals = weekend_df['Accidents']
    else:
        x_vals = weekend_df.iloc[:, 0]
        y_vals = weekend_df.iloc[:, 1]
    
    bars = plt.bar(x_vals, y_vals, color=colors_wk, edgecolor='black')
    plt.xlabel('Day Type', fontsize=14)
    plt.ylabel('Number of Accidents', fontsize=14)
    plt.title('Weekend vs Weekday Accidents', fontsize=16, fontweight='bold')

    for bar, count in zip(bars, y_vals):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5000, 
                 f'{int(count):,}', ha='center', va='bottom', fontsize=12)

    plt.tight_layout()
    plt.savefig("outputs/figures/08_weekend_vs_weekday.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("   ✅ Saved: 08_weekend_vs_weekday.png")
else:
    print("   ❌ Skipped: weekend_vs_weekday.csv not found")

# =========================================================
# CHART 9: DAY vs NIGHT (FIXED PATH)
# =========================================================
print("\n📊 Creating Chart 9: Day vs Night...")

day_night_df = safe_read_csv("outputs/statistical_analysis/tables/05_day_vs_night.csv")

if day_night_df is not None:
    plt.figure(figsize=(8, 6))
    colors_dn = ['#f1c40f', '#2c3e50']
    
    # Handle column names
    if 'Period' in day_night_df.columns:
        x_vals = day_night_df['Period']
        y_vals = day_night_df['Accidents']
    else:
        x_vals = day_night_df.iloc[:, 0]
        y_vals = day_night_df.iloc[:, 1]
    
    bars = plt.bar(x_vals, y_vals, color=colors_dn, edgecolor='black')
    plt.xlabel('Time Period', fontsize=14)
    plt.ylabel('Number of Accidents', fontsize=14)
    plt.title('Day vs Night Accidents', fontsize=16, fontweight='bold')

    for bar, count in zip(bars, y_vals):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 3000, 
                 f'{int(count):,}', ha='center', va='bottom', fontsize=12)

    plt.tight_layout()
    plt.savefig("outputs/figures/09_day_vs_night.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("   ✅ Saved: 09_day_vs_night.png")
else:
    print("   ❌ Skipped: day_vs_night.csv not found")

# =========================================================
# CHART 10: SEASONAL ANALYSIS
# =========================================================
print("\n📊 Creating Chart 10: Seasonal Analysis...")

season_df = safe_read_csv("outputs/advanced_features/tables/02_seasonal_analysis.csv")

if season_df is not None:
    season_order = ['Spring', 'Summer', 'Fall', 'Winter']
    season_df['Season'] = pd.Categorical(season_df['Season'], categories=season_order, ordered=True)
    season_df = season_df.sort_values('Season')

    plt.figure(figsize=(10, 6))
    colors_season = ['#2ecc71', '#f39c12', '#e74c3c', '#3498db']
    bars = plt.bar(season_df['Season'], season_df['Avg_Severity'], 
                   color=colors_season, edgecolor='black')
    plt.xlabel('Season', fontsize=14)
    plt.ylabel('Average Severity', fontsize=14)
    plt.title('Accident Severity by Season', fontsize=16, fontweight='bold')
    plt.ylim(2.4, 2.52)

    for bar, severity in zip(bars, season_df['Avg_Severity']):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.005, 
                 f'{severity:.3f}', ha='center', va='bottom', fontsize=11)

    plt.tight_layout()
    plt.savefig("outputs/figures/10_seasonal_analysis.png", dpi=300, bbox_inches='tight')
    plt.close()
    print("   ✅ Saved: 10_seasonal_analysis.png")

# =========================================================
# SUMMARY
# =========================================================
print("\n" + "=" * 80)
print("📊 VISUALIZATION SUMMARY")
print("=" * 80)
print("""
✅ VISUALIZATION COMPLETE!

📁 Figures saved to: outputs/figures/

Created charts:
   01_severity_distribution.png
   02_time_of_day_distribution.png
   03_ga_vs_ct_severity.png
   04_keyword_severity_impact.png
   05_road_features_impact.png
   06_most_dangerous_cities.png
   07_risk_combinations.png
   08_weekend_vs_weekday.png
   09_day_vs_night.png
   10_seasonal_analysis.png
""")

print("=" * 80)
print("✨ VISUALIZATION COMPLETE! ✨")
print("=" * 80)

if __name__ == "__main__":
    print("\n✅ Visualization module ready")