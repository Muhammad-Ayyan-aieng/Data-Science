# statistical_analysis.py
"""
Step 3: Statistical Analysis of Cleaned Accident Data
Calculates central tendency, dispersion, correlations, and categorical distributions
Exports ALL results to CSV files for visualization and reporting
"""

import pandas as pd
import numpy as np
import os
from scipy import stats

def run_statistical_analysis():
    """Main function to perform statistical analysis on cleaned data"""
    
    print("=" * 70)
    print("📊 STATISTICAL ANALYSIS - GA & CT ACCIDENTS")
    print("=" * 70)
    
    # Create output folders
    os.makedirs("outputs/tables", exist_ok=True)
    os.makedirs("outputs/reports", exist_ok=True)
    
    # Define file path
    input_file = os.path.join("datasets", "cleaned_accidents.csv")
    
    # Check if cleaned data exists
    if not os.path.exists(input_file):
        print(f"\n❌ ERROR: {input_file} not found!")
        print("   Please run data_cleaning.py first")
        return None
    
    # Load cleaned data
    print(f"\n📂 Loading {input_file}...")
    df = pd.read_csv(input_file)
    print(f"✅ Loaded {len(df):,} accidents")
    print(f"✅ Columns: {len(df.columns)}")
    
    # ============================================
    # SECTION 1: NUMERICAL FEATURES ANALYSIS
    # ============================================
    print("\n" + "=" * 70)
    print("SECTION 1: NUMERICAL FEATURES ANALYSIS")
    print("=" * 70)
    
    # Select numerical columns for analysis
    numerical_cols = ['Severity', 'Temperature(F)', 'Humidity(%)', 
                      'Pressure(in)', 'Visibility(mi)', 'Wind_Speed(mph)', 
                      'Precipitation(in)', 'Distance(mi)', 'Hour', 'Month', 
                      'DayOfWeek', 'Duration_Minutes']
    
    # Filter only columns that exist in dataframe
    available_num_cols = [col for col in numerical_cols if col in df.columns]
    
    print(f"\n📊 Analyzing {len(available_num_cols)} numerical features:\n")
    print(f"{'Feature':<20} {'Mean':<12} {'Median':<12} {'Std Dev':<12} {'Min':<10} {'Max':<10} {'Range':<12}")
    print("-" * 95)
    
    stats_summary = []
    
    for col in available_num_cols:
        mean_val = df[col].mean()
        median_val = df[col].median()
        std_val = df[col].std()
        min_val = df[col].min()
        max_val = df[col].max()
        range_val = max_val - min_val
        
        print(f"{col:<20} {mean_val:<12.2f} {median_val:<12.2f} {std_val:<12.2f} {min_val:<10.2f} {max_val:<10.2f} {range_val:<12.2f}")
        
        stats_summary.append({
            'Feature': col,
            'Mean': round(mean_val, 4),
            'Median': round(median_val, 4),
            'Std_Dev': round(std_val, 4),
            'Min': round(min_val, 4),
            'Max': round(max_val, 4),
            'Range': round(range_val, 4)
        })
    
    # Save numerical statistics to CSV
    stats_df = pd.DataFrame(stats_summary)
    stats_output = os.path.join("outputs/tables", "numerical_statistics.csv")
    stats_df.to_csv(stats_output, index=False)
    print(f"\n✅ Saved: {stats_output}")
    
    # ============================================
    # SECTION 2: QUARTILES AND PERCENTILES
    # ============================================
    print("\n" + "=" * 70)
    print("SECTION 2: QUARTILES & PERCENTILES")
    print("=" * 70)
    
    print(f"\n📊 Percentile Analysis for Key Features:\n")
    
    key_features = ['Severity', 'Temperature(F)', 'Humidity(%)', 'Duration_Minutes']
    key_features = [col for col in key_features if col in df.columns]
    
    print(f"{'Feature':<20} {'25% (Q1)':<12} {'50% (Median)':<12} {'75% (Q3)':<12} {'IQR':<12}")
    print("-" * 70)
    
    percentile_results = []
    
    for col in key_features:
        q1 = df[col].quantile(0.25)
        q2 = df[col].quantile(0.50)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        
        print(f"{col:<20} {q1:<12.2f} {q2:<12.2f} {q3:<12.2f} {iqr:<12.2f}")
        
        percentile_results.append({
            'Feature': col,
            'Q1_25%': round(q1, 4),
            'Median_50%': round(q2, 4),
            'Q3_75%': round(q3, 4),
            'IQR': round(iqr, 4)
        })
    
    # Save percentile results to CSV
    percentile_df = pd.DataFrame(percentile_results)
    percentile_output = os.path.join("outputs/tables", "percentile_analysis.csv")
    percentile_df.to_csv(percentile_output, index=False)
    print(f"\n✅ Saved: {percentile_output}")
    
    # ============================================
    # SECTION 3: CORRELATION ANALYSIS
    # ============================================
    print("\n" + "=" * 70)
    print("SECTION 3: CORRELATION ANALYSIS")
    print("=" * 70)
    
    # Calculate correlation matrix
    corr_matrix = df[available_num_cols].corr()
    
    # Save full correlation matrix to CSV
    corr_output = os.path.join("outputs/tables", "full_correlation_matrix.csv")
    corr_matrix.to_csv(corr_output)
    print(f"\n✅ Saved full correlation matrix: {corr_output}")
    
    correlation_results = []
    
    # Find correlations with Severity (target variable)
    if 'Severity' in corr_matrix.columns:
        print(f"\n📈 Correlation with Accident Severity:\n")
        severity_corr = corr_matrix['Severity'].sort_values(ascending=False)
        
        print(f"{'Feature':<25} {'Correlation with Severity':<25} {'Interpretation':<20}")
        print("-" * 70)
        
        for feature, corr_value in severity_corr.items():
            if feature != 'Severity':
                if corr_value > 0.5:
                    interpretation = "Strong Positive"
                elif corr_value > 0.3:
                    interpretation = "Moderate Positive"
                elif corr_value > 0.1:
                    interpretation = "Weak Positive"
                elif corr_value > -0.1:
                    interpretation = "No Correlation"
                elif corr_value > -0.3:
                    interpretation = "Weak Negative"
                elif corr_value > -0.5:
                    interpretation = "Moderate Negative"
                else:
                    interpretation = "Strong Negative"
                
                print(f"{feature:<25} {corr_value:<25.4f} {interpretation:<20}")
                
                correlation_results.append({
                    'Feature': feature,
                    'Correlation_with_Severity': round(corr_value, 4),
                    'Interpretation': interpretation
                })
    
    # Save correlation results to CSV
    correlation_df = pd.DataFrame(correlation_results)
    correlation_summary_output = os.path.join("outputs/tables", "severity_correlations.csv")
    correlation_df.to_csv(correlation_summary_output, index=False)
    print(f"\n✅ Saved: {correlation_summary_output}")
    
    # ============================================
    # SECTION 4: CATEGORICAL FEATURES ANALYSIS
    # ============================================
    print("\n" + "=" * 70)
    print("SECTION 4: CATEGORICAL FEATURES ANALYSIS")
    print("=" * 70)
    
    # 4.1 Severity distribution
    severity_distribution_results = []
    
    if 'Severity' in df.columns:
        print(f"\n📊 Accident Severity Distribution:")
        print(f"{'Severity':<12} {'Count':<12} {'Percentage':<12} {'Cumulative':<12}")
        print("-" * 50)
        
        severity_counts = df['Severity'].value_counts().sort_index()
        total = len(df)
        cumulative = 0
        
        for severity, count in severity_counts.items():
            pct = (count / total) * 100
            cumulative += pct
            print(f"Severity {severity:<5} {count:<12,} {pct:<11.2f}% {cumulative:<11.2f}%")
            
            severity_distribution_results.append({
                'Severity': severity,
                'Count': int(count),
                'Percentage': round(pct, 2),
                'Cumulative_Percentage': round(cumulative, 2)
            })
    
    # Save severity distribution to CSV
    severity_dist_df = pd.DataFrame(severity_distribution_results)
    severity_output = os.path.join("outputs/tables", "severity_distribution.csv")
    severity_dist_df.to_csv(severity_output, index=False)
    print(f"\n✅ Saved: {severity_output}")
    
    # 4.2 State distribution
    if 'State' in df.columns:
        print(f"\n📊 State-wise Accident Distribution:")
        state_counts = df['State'].value_counts()
        
        state_results = []
        for state, count in state_counts.items():
            pct = (count / len(df)) * 100
            print(f"   {state}: {count:,} accidents ({pct:.1f}%)")
            state_results.append({
                'State': state,
                'Accident_Count': int(count),
                'Percentage': round(pct, 2)
            })
        
        state_df = pd.DataFrame(state_results)
        state_output = os.path.join("outputs/tables", "state_distribution.csv")
        state_df.to_csv(state_output, index=False)
        print(f"\n✅ Saved: {state_output}")
    
    # 4.3 Time of day distribution
    if 'TimeOfDay' in df.columns:
        print(f"\n📊 Time of Day Distribution:")
        time_order = ['Late Night', 'Morning', 'Afternoon', 'Evening', 'Night']
        time_counts = df['TimeOfDay'].value_counts()
        
        time_results = []
        for time in time_order:
            if time in time_counts:
                count = time_counts[time]
                pct = (count / len(df)) * 100
                print(f"   {time}: {count:,} accidents ({pct:.1f}%)")
                time_results.append({
                    'TimeOfDay': time,
                    'Accident_Count': int(count),
                    'Percentage': round(pct, 2)
                })
        
        time_df = pd.DataFrame(time_results)
        time_output = os.path.join("outputs/tables", "time_of_day_distribution.csv")
        time_df.to_csv(time_output, index=False)
        print(f"\n✅ Saved: {time_output}")
    
    # 4.4 Day vs Night distribution
    if 'Sunrise_Sunset' in df.columns:
        print(f"\n📊 Day vs Night Accidents:")
        day_night = df['Sunrise_Sunset'].value_counts()
        
        day_night_results = []
        for category, count in day_night.items():
            pct = (count / len(df)) * 100
            print(f"   {category}: {count:,} accidents ({pct:.1f}%)")
            day_night_results.append({
                'Period': category,
                'Accident_Count': int(count),
                'Percentage': round(pct, 2)
            })
        
        day_night_df = pd.DataFrame(day_night_results)
        day_night_output = os.path.join("outputs/tables", "day_night_distribution.csv")
        day_night_df.to_csv(day_night_output, index=False)
        print(f"\n✅ Saved: {day_night_output}")
    
    # 4.5 Weekend vs Weekday
    if 'IsWeekend' in df.columns:
        print(f"\n📊 Weekend vs Weekday Accidents:")
        weekend_count = df[df['IsWeekend'] == 1].shape[0]
        weekday_count = df[df['IsWeekend'] == 0].shape[0]
        weekend_pct = (weekend_count / len(df)) * 100
        weekday_pct = (weekday_count / len(df)) * 100
        
        print(f"   Weekend: {weekend_count:,} accidents ({weekend_pct:.1f}%)")
        print(f"   Weekday: {weekday_count:,} accidents ({weekday_pct:.1f}%)")
        
        weekend_results = [
            {'Day_Type': 'Weekend', 'Accident_Count': int(weekend_count), 'Percentage': round(weekend_pct, 2)},
            {'Day_Type': 'Weekday', 'Accident_Count': int(weekday_count), 'Percentage': round(weekday_pct, 2)}
        ]
        
        weekend_df = pd.DataFrame(weekend_results)
        weekend_output = os.path.join("outputs/tables", "weekend_weekday_distribution.csv")
        weekend_df.to_csv(weekend_output, index=False)
        print(f"\n✅ Saved: {weekend_output}")
    
    # 4.6 Weather conditions (top 10)
    if 'Weather_Condition' in df.columns:
        print(f"\n📊 Top 10 Weather Conditions:")
        weather_counts = df['Weather_Condition'].value_counts().head(10)
        
        weather_results = []
        for weather, count in weather_counts.items():
            pct = (count / len(df)) * 100
            print(f"   {weather}: {count:,} accidents ({pct:.1f}%)")
            weather_results.append({
                'Weather_Condition': weather,
                'Accident_Count': int(count),
                'Percentage': round(pct, 2)
            })
        
        weather_df = pd.DataFrame(weather_results)
        weather_output = os.path.join("outputs/tables", "top_10_weather_conditions.csv")
        weather_df.to_csv(weather_output, index=False)
        print(f"\n✅ Saved: {weather_output}")
    
    # ============================================
    # SECTION 5: GA vs CT COMPARISON
    # ============================================
    print("\n" + "=" * 70)
    print("SECTION 5: GEORGIA vs CONNECTICUT COMPARISON")
    print("=" * 70)
    
    ga_ct_results = []
    
    if 'State' in df.columns:
        for state in ['GA', 'CT']:
            state_df = df[df['State'] == state]
            print(f"\n📊 {state} Statistics:")
            print(f"   Total Accidents: {len(state_df):,}")
            print(f"   Average Severity: {state_df['Severity'].mean():.2f}")
            
            result = {
                'State': state,
                'Total_Accidents': len(state_df),
                'Average_Severity': round(state_df['Severity'].mean(), 4),
                'Most_Common_Severity': int(state_df['Severity'].mode()[0])
            }
            
            if 'Temperature(F)' in df.columns:
                temp = state_df['Temperature(F)'].mean()
                print(f"   Average Temperature: {temp:.1f}°F")
                result['Average_Temperature_F'] = round(temp, 2)
            
            if 'Humidity(%)' in df.columns:
                humidity = state_df['Humidity(%)'].mean()
                print(f"   Average Humidity: {humidity:.1f}%")
                result['Average_Humidity_Pct'] = round(humidity, 2)
            
            if 'Precipitation(in)' in df.columns:
                precip = state_df['Precipitation(in)'].mean()
                print(f"   Average Precipitation: {precip:.2f} inches")
                result['Average_Precipitation_in'] = round(precip, 4)
            
            if 'Duration_Minutes' in df.columns:
                duration = state_df['Duration_Minutes'].mean()
                print(f"   Average Duration: {duration:.1f} minutes")
                result['Average_Duration_Minutes'] = round(duration, 2)
            
            if 'TimeOfDay' in df.columns:
                top_time = state_df['TimeOfDay'].mode()[0]
                print(f"   Most Common Time: {top_time}")
                result['Most_Common_TimeOfDay'] = top_time
            
            ga_ct_results.append(result)
    
    # Save GA vs CT comparison to CSV
    ga_ct_df = pd.DataFrame(ga_ct_results)
    ga_ct_output = os.path.join("outputs/tables", "ga_vs_ct_comparison.csv")
    ga_ct_df.to_csv(ga_ct_output, index=False)
    print(f"\n✅ Saved: {ga_ct_output}")
    
    # ============================================
    # SECTION 6: SAVE CORRELATION MATRIX (again for datasets folder)
    # ============================================
    print("\n" + "=" * 70)
    print("SECTION 6: SAVING ADDITIONAL REPORTS")
    print("=" * 70)
    
    # Also save to datasets folder for backward compatibility
    stats_output_legacy = os.path.join("datasets", "statistical_summary.csv")
    stats_df.to_csv(stats_output_legacy, index=False)
    print(f"✅ Statistical summary saved to: {stats_output_legacy}")
    
    corr_output_legacy = os.path.join("datasets", "correlation_matrix.csv")
    corr_matrix.to_csv(corr_output_legacy)
    print(f"✅ Correlation matrix saved to: {corr_output_legacy}")
    
    # Save summary report as text file
    with open("outputs/reports/statistical_analysis_summary.txt", "w") as f:
        f.write("=" * 70 + "\n")
        f.write("STATISTICAL ANALYSIS SUMMARY\n")
        f.write("=" * 70 + "\n\n")
        f.write(f"Total Accidents Analyzed: {len(df):,}\n")
        f.write(f"States: GA ({len(df[df['State']=='GA']):,}), CT ({len(df[df['State']=='CT']):,})\n")
        f.write(f"Average Severity: {df['Severity'].mean():.2f} (Range: 1-4)\n")
        f.write(f"Most Common Severity: {df['Severity'].mode()[0]}\n\n")
        f.write("=" * 70 + "\n")
        f.write("CORRELATION WITH SEVERITY (Top 5)\n")
        f.write("=" * 70 + "\n")
        for corr in correlation_results[:5]:
            f.write(f"{corr['Feature']}: {corr['Correlation_with_Severity']} ({corr['Interpretation']})\n")
    
    print(f"✅ Saved: outputs/reports/statistical_analysis_summary.txt")
    
    # ============================================
    # SECTION 7: SUMMARY
    # ============================================
    print("\n" + "=" * 70)
    print("📊 STATISTICAL ANALYSIS SUMMARY")
    print("=" * 70)
    
    print(f"""
✅ Analysis Complete!

Key Findings:
--------------
• Total Accidents Analyzed: {len(df):,}
• States: GA ({len(df[df['State']=='GA']):,}), CT ({len(df[df['State']=='CT']):,})
• Average Severity: {df['Severity'].mean():.2f} (Range: 1-4)
• Most Common Severity: {df['Severity'].mode()[0]}

📁 ALL CSV FILES CREATED:
------------------------
outputs/tables/
   ├── numerical_statistics.csv          (Mean, median, std for all numerical features)
   ├── percentile_analysis.csv           (Q1, Median, Q3, IQR for key features)
   ├── full_correlation_matrix.csv       (Complete correlation matrix)
   ├── severity_correlations.csv         (Correlations with severity only)
   ├── severity_distribution.csv         (Count and % for each severity level)
   ├── state_distribution.csv            (GA vs CT accident counts)
   ├── time_of_day_distribution.csv      (Accidents by time period)
   ├── day_night_distribution.csv        (Day vs Night accidents)
   ├── weekend_weekday_distribution.csv  (Weekend vs Weekday)
   ├── top_10_weather_conditions.csv     (Most common weather conditions)
   └── ga_vs_ct_comparison.csv           (Comprehensive state comparison)

outputs/reports/
   └── statistical_analysis_summary.txt  (Plain text summary)

datasets/
   ├── statistical_summary.csv           (Legacy - numerical statistics)
   └── correlation_matrix.csv            (Legacy - correlation matrix)
""")
    
    print("=" * 70)
    print("✨ STATISTICAL ANALYSIS COMPLETE! ✨")
    print("=" * 70)
    
    return df, stats_df, corr_matrix

# Auto-run when imported
if __name__ == "__main__" or __name__ == "statistical_analysis":
    run_statistical_analysis()