# visualization.py
"""
Step 4: Create Professional Visualizations from All Analysis Results
Generates charts for report using CSV outputs from statistical, text, and advanced analysis
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

print("=" * 70)
print("🎨 VISUALIZATION - CREATING CHARTS FOR REPORT")
print("=" * 70)


# =========================================================
# CHART 1: SEVERITY DISTRIBUTION (Pie Chart + Bar Chart)
# =========================================================
print("\n📊 Creating Chart 1: Severity Distribution...")

# Load severity distribution
severity_df = pd.read_csv("outputs/tables/severity_distribution.csv")

# Bar Chart
plt.figure(figsize=(10, 6))
colors = ['#2ecc71', '#f39c12', '#e74c3c', '#c0392b']
bars = plt.bar(severity_df['Severity'].astype(str), severity_df['Count'], color=colors, edgecolor='black')
plt.xlabel('Severity Level', fontsize=14)
plt.ylabel('Number of Accidents', fontsize=14)
plt.title('Accident Severity Distribution (GA & CT)', fontsize=16, fontweight='bold')

# Add value labels on bars
for bar, count in zip(bars, severity_df['Count']):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5000, 
             f'{count:,}', ha='center', va='bottom', fontsize=11)

plt.tight_layout()
plt.savefig("outputs/figures/severity_distribution_bar.png", dpi=300, bbox_inches='tight')
plt.close()

# Pie Chart
plt.figure(figsize=(8, 8))
plt.pie(severity_df['Count'], labels=[f'Severity {s}' for s in severity_df['Severity']], 
        autopct='%1.1f%%', colors=colors, startangle=90, explode=(0, 0.05, 0.1, 0.15))
plt.title('Accident Severity Distribution (GA & CT)', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig("outputs/figures/severity_distribution_pie.png", dpi=300, bbox_inches='tight')
plt.close()
print("   ✅ Saved: severity_distribution_bar.png, severity_distribution_pie.png")


# =========================================================
# CHART 2: TIME OF DAY DISTRIBUTION
# =========================================================
print("\n📊 Creating Chart 2: Time of Day Distribution...")

time_df = pd.read_csv("outputs/tables/time_of_day_distribution.csv")

# Define order
time_order = ['Late Night', 'Morning', 'Afternoon', 'Evening', 'Night']
time_df['TimeOfDay'] = pd.Categorical(time_df['TimeOfDay'], categories=time_order, ordered=True)
time_df = time_df.sort_values('TimeOfDay')

plt.figure(figsize=(12, 6))
colors_bar = ['#34495e', '#e74c3c', '#f39c12', '#2ecc71', '#3498db']
bars = plt.bar(time_df['TimeOfDay'], time_df['Accident_Count'], color=colors_bar, edgecolor='black')
plt.xlabel('Time of Day', fontsize=14)
plt.ylabel('Number of Accidents', fontsize=14)
plt.title('Accident Distribution by Time of Day', fontsize=16, fontweight='bold')

# Add value labels
for bar, count in zip(bars, time_df['Accident_Count']):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2000, 
             f'{count:,}', ha='center', va='bottom', fontsize=10)

plt.tight_layout()
plt.savefig("outputs/figures/time_of_day_distribution.png", dpi=300, bbox_inches='tight')
plt.close()
print("   ✅ Saved: time_of_day_distribution.png")


# =========================================================
# CHART 3: GA vs CT COMPARISON (Grouped Bar Chart)
# =========================================================
print("\n📊 Creating Chart 3: GA vs CT Comparison...")

ga_ct_df = pd.read_csv("outputs/tables/ga_vs_ct_comparison.csv")

plt.figure(figsize=(10, 6))
states = ga_ct_df['State']
severities = ga_ct_df['Average_Severity']
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
plt.savefig("outputs/figures/ga_vs_ct_severity.png", dpi=300, bbox_inches='tight')
plt.close()
print("   ✅ Saved: ga_vs_ct_severity.png")


# =========================================================
# CHART 4: TOP 10 WEATHER CONDITIONS
# =========================================================
print("\n📊 Creating Chart 4: Top 10 Weather Conditions...")

weather_df = pd.read_csv("outputs/tables/top_10_weather_conditions.csv")

plt.figure(figsize=(12, 8))
bars = plt.barh(weather_df['Weather_Condition'], weather_df['Accident_Count'], 
                color='#3498db', edgecolor='black')
plt.xlabel('Number of Accidents', fontsize=14)
plt.ylabel('Weather Condition', fontsize=14)
plt.title('Top 10 Weather Conditions for Accidents', fontsize=16, fontweight='bold')
plt.gca().invert_yaxis()

# Add value labels
for bar, count in zip(bars, weather_df['Accident_Count']):
    plt.text(bar.get_width() + 1000, bar.get_y() + bar.get_height()/2, 
             f'{count:,}', ha='left', va='center', fontsize=10)

plt.tight_layout()
plt.savefig("outputs/figures/top_10_weather_conditions.png", dpi=300, bbox_inches='tight')
plt.close()
print("   ✅ Saved: top_10_weather_conditions.png")


# =========================================================
# CHART 5: SPECIFIC KEYWORD SEVERITY IMPACT
# =========================================================
print("\n📊 Creating Chart 5: Keyword Severity Impact...")

keyword_df = pd.read_csv("outputs/tables/specific_keyword_analysis.csv")

# Sort by severity
keyword_df = keyword_df.sort_values('Avg_Severity', ascending=False)

plt.figure(figsize=(12, 8))
colors_keyword = ['#c0392b' if x > 2.6 else '#e74c3c' if x > 2.4 else '#f39c12' if x > 2.2 else '#2ecc71' 
                  for x in keyword_df['Avg_Severity']]
bars = plt.barh(keyword_df['Keyword'], keyword_df['Avg_Severity'], color=colors_keyword, edgecolor='black')
plt.xlabel('Average Severity', fontsize=14)
plt.ylabel('Keyword', fontsize=14)
plt.title('Impact of Keywords on Accident Severity', fontsize=16, fontweight='bold')
plt.xlim(2.0, 3.2)
plt.axvline(x=2.46, color='gray', linestyle='--', label='Overall Average Severity (2.46)')
plt.legend()

# Add value labels
for bar, severity in zip(bars, keyword_df['Avg_Severity']):
    plt.text(bar.get_width() + 0.02, bar.get_y() + bar.get_height()/2, 
             f'{severity:.2f}', ha='left', va='center', fontsize=10)

plt.tight_layout()
plt.savefig("outputs/figures/keyword_severity_impact.png", dpi=300, bbox_inches='tight')
plt.close()
print("   ✅ Saved: keyword_severity_impact.png")


# =========================================================
# CHART 6: ROAD FEATURES IMPACT (Positive vs Negative)
# =========================================================
print("\n📊 Creating Chart 6: Road Features Impact...")

road_df = pd.read_csv("outputs/tables/road_features_analysis.csv")

# Filter out NaN values and sort by difference
road_df = road_df.dropna(subset=['Difference'])
road_df = road_df.sort_values('Difference', ascending=False)

# Color: green for positive (worse), red for negative (better)
colors_road = ['#e74c3c' if x > 0 else '#2ecc71' for x in road_df['Difference']]

plt.figure(figsize=(14, 10))
bars = plt.barh(road_df['Feature'], road_df['Difference'], color=colors_road, edgecolor='black')
plt.xlabel('Difference in Severity (Present - Absent)', fontsize=14)
plt.ylabel('Road Feature', fontsize=14)
plt.title('Impact of Road Features on Accident Severity', fontsize=16, fontweight='bold')
plt.axvline(x=0, color='black', linestyle='-', linewidth=1)

# Add value labels
for bar, diff in zip(bars, road_df['Difference']):
    plt.text(bar.get_width() + 0.01 if diff > 0 else bar.get_width() - 0.08, 
             bar.get_y() + bar.get_height()/2, 
             f'{diff:+.3f}', ha='left' if diff > 0 else 'right', va='center', fontsize=9)

plt.tight_layout()
plt.savefig("outputs/figures/road_features_impact.png", dpi=300, bbox_inches='tight')
plt.close()
print("   ✅ Saved: road_features_impact.png")


# =========================================================
# CHART 7: TOP 10 MOST DANGEROUS CITIES
# =========================================================
print("\n📊 Creating Chart 7: Top 10 Most Dangerous Cities...")

city_df = pd.read_csv("outputs/tables/city_analysis.csv")
dangerous_cities = city_df.head(10)

plt.figure(figsize=(12, 8))
bars = plt.barh(dangerous_cities['City'], dangerous_cities['Avg_Severity'], 
                color='#e74c3c', edgecolor='black')
plt.xlabel('Average Severity', fontsize=14)
plt.ylabel('City', fontsize=14)
plt.title('Top 10 Most Dangerous Cities (Highest Average Severity)', fontsize=16, fontweight='bold')
plt.xlim(2.5, 3.2)
plt.gca().invert_yaxis()

for bar, severity in zip(bars, dangerous_cities['Avg_Severity']):
    plt.text(bar.get_width() + 0.02, bar.get_y() + bar.get_height()/2, 
             f'{severity:.2f}', ha='left', va='center', fontsize=10)

plt.tight_layout()
plt.savefig("outputs/figures/most_dangerous_cities.png", dpi=300, bbox_inches='tight')
plt.close()
print("   ✅ Saved: most_dangerous_cities.png")


# =========================================================
# CHART 8: RISK COMBINATIONS COMPARISON
# =========================================================
print("\n📊 Creating Chart 8: Risk Combinations Comparison...")

risk_df = pd.read_csv("outputs/tables/risk_combinations.csv")

plt.figure(figsize=(12, 8))
colors_risk = ['#e74c3c' if x > 2.6 else '#f39c12' if x > 2.5 else '#2ecc71' 
               for x in risk_df['Avg_Severity']]
bars = plt.barh(risk_df['Combination'], risk_df['Avg_Severity'], color=colors_risk, edgecolor='black')
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
plt.savefig("outputs/figures/risk_combinations.png", dpi=300, bbox_inches='tight')
plt.close()
print("   ✅ Saved: risk_combinations.png")


# =========================================================
# CHART 9: CORRELATION HEATMAP
# =========================================================
print("\n📊 Creating Chart 9: Correlation Heatmap...")

corr_matrix = pd.read_csv("datasets/correlation_matrix.csv", index_col=0)

plt.figure(figsize=(14, 12))
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
sns.heatmap(corr_matrix, mask=mask, annot=True, fmt='.2f', cmap='RdBu_r', 
            center=0, square=True, linewidths=0.5, cbar_kws={"shrink": 0.8},
            annot_kws={'size': 8})
plt.title('Correlation Matrix of Numerical Features', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig("outputs/figures/correlation_heatmap.png", dpi=300, bbox_inches='tight')
plt.close()
print("   ✅ Saved: correlation_heatmap.png")


# =========================================================
# CHART 10: WEEKEND vs WEEKDAY
# =========================================================
print("\n📊 Creating Chart 10: Weekend vs Weekday...")

weekend_df = pd.read_csv("outputs/tables/weekend_weekday_distribution.csv")

plt.figure(figsize=(8, 6))
colors_wk = ['#f39c12', '#3498db']
bars = plt.bar(weekend_df['Day_Type'], weekend_df['Accident_Count'], color=colors_wk, edgecolor='black')
plt.xlabel('Day Type', fontsize=14)
plt.ylabel('Number of Accidents', fontsize=14)
plt.title('Weekend vs Weekday Accidents', fontsize=16, fontweight='bold')

for bar, count in zip(bars, weekend_df['Accident_Count']):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5000, 
             f'{count:,}', ha='center', va='bottom', fontsize=12)

plt.tight_layout()
plt.savefig("outputs/figures/weekend_vs_weekday.png", dpi=300, bbox_inches='tight')
plt.close()
print("   ✅ Saved: weekend_vs_weekday.png")


# =========================================================
# CHART 11: DAY vs NIGHT
# =========================================================
print("\n📊 Creating Chart 11: Day vs Night...")

day_night_df = pd.read_csv("outputs/tables/day_night_distribution.csv")

plt.figure(figsize=(8, 6))
colors_dn = ['#f1c40f', '#2c3e50']
bars = plt.bar(day_night_df['Period'], day_night_df['Accident_Count'], color=colors_dn, edgecolor='black')
plt.xlabel('Time Period', fontsize=14)
plt.ylabel('Number of Accidents', fontsize=14)
plt.title('Day vs Night Accidents', fontsize=16, fontweight='bold')

for bar, count in zip(bars, day_night_df['Accident_Count']):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 3000, 
             f'{count:,}', ha='center', va='bottom', fontsize=12)

plt.tight_layout()
plt.savefig("outputs/figures/day_vs_night.png", dpi=300, bbox_inches='tight')
plt.close()
print("   ✅ Saved: day_vs_night.png")


# =========================================================
# CHART 12: WIND CHILL SEVERITY
# =========================================================
print("\n📊 Creating Chart 12: Wind Chill Severity...")

windchill_df = pd.read_csv("outputs/tables/windchill_analysis.csv")

plt.figure(figsize=(10, 6))
bars = plt.bar(windchill_df['Category'], windchill_df['Avg_Severity'], 
               color='#3498db', edgecolor='black')
plt.xlabel('Temperature Category', fontsize=14)
plt.ylabel('Average Severity', fontsize=14)
plt.title('Accident Severity by Temperature Category', fontsize=16, fontweight='bold')
plt.ylim(2.3, 2.45)
plt.axhline(y=2.46, color='red', linestyle='--', label='Overall Average (2.46)')
plt.legend()

for bar, severity in zip(bars, windchill_df['Avg_Severity']):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01, 
             f'{severity:.2f}', ha='center', va='bottom', fontsize=11)

plt.tight_layout()
plt.savefig("outputs/figures/windchill_severity.png", dpi=300, bbox_inches='tight')
plt.close()
print("   ✅ Saved: windchill_severity.png")


# =========================================================
# SUMMARY
# =========================================================
print("\n" + "=" * 70)
print("📊 VISUALIZATION SUMMARY")
print("=" * 70)
print("""
✅ ALL CHARTS CREATED SUCCESSFULLY!

📁 Figures saved to: outputs/figures/

┌────────────────────────────────┬────────────────────────────────────┐
│ Chart Name                     │ File Name                          │
├────────────────────────────────┼────────────────────────────────────┤
│ Severity Distribution (Bar)    │ severity_distribution_bar.png      │
│ Severity Distribution (Pie)    │ severity_distribution_pie.png      │
│ Time of Day Distribution       │ time_of_day_distribution.png       │
│ GA vs CT Comparison            │ ga_vs_ct_severity.png              │
│ Top 10 Weather Conditions      │ top_10_weather_conditions.png      │
│ Keyword Severity Impact        │ keyword_severity_impact.png        │
│ Road Features Impact           │ road_features_impact.png           │
│ Most Dangerous Cities          │ most_dangerous_cities.png          │
│ Risk Combinations              │ risk_combinations.png              │
│ Correlation Heatmap            │ correlation_heatmap.png            │
│ Weekend vs Weekday             │ weekend_vs_weekday.png             │
│ Day vs Night                   │ day_vs_night.png                   │
│ Wind Chill Severity            │ windchill_severity.png             │
└────────────────────────────────┴────────────────────────────────────┘

🎯 These charts are ready to be inserted into your report!
""")

print("=" * 70)
print("✨ VISUALIZATION COMPLETE! ✨")
print("=" * 70)


if __name__ == "__main__" or __name__ == "visualization":
    print("\n✅ Visualization module loaded. Run this file directly to create charts.")