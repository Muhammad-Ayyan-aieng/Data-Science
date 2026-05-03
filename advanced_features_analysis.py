# advanced_features_analysis.py
"""
Advanced Analysis of All Dataset Features
Calculates statistics for road features, geographic patterns, and risk factors
Outputs CSV files for visualization.py to use
"""

import pandas as pd
import numpy as np
import os
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

def analyze_all_features():
    """Complete analysis of all unused columns - saves results for visualization"""
    
    print("=" * 70)
    print("🔍 ADVANCED FEATURES ANALYSIS - DATA CALCULATION ONLY")
    print("=" * 70)
    
    # Create output folder for tables
    os.makedirs("outputs/tables", exist_ok=True)
    
    # Load data
    input_file = os.path.join("datasets", "cleaned_accidents.csv")
    df = pd.read_csv(input_file)
    print(f"✅ Loaded {len(df):,} accidents")
    
    all_results = {}  # Store all results for final summary
    
    # =========================================================
    # 1. ROAD FEATURES IMPACT ANALYSIS
    # =========================================================
    print("\n" + "-" * 50)
    print("1. ROAD FEATURES IMPACT ON SEVERITY")
    print("-" * 50)
    
    road_features = ['Amenity', 'Bump', 'Crossing', 'Give_Way', 'Junction', 
                     'No_Exit', 'Railway', 'Roundabout', 'Station', 'Stop', 
                     'Traffic_Calming', 'Traffic_Signal', 'Turning_Loop']
    
    road_results = []
    
    for feature in road_features:
        if feature in df.columns:
            # Calculate statistics
            true_mask = df[feature] == True
            false_mask = df[feature] == False
            
            true_count = true_mask.sum()
            false_count = false_mask.sum()
            
            true_severity = df[true_mask]['Severity'].mean()
            false_severity = df[false_mask]['Severity'].mean()
            severity_diff = true_severity - false_severity
            
            # Calculate severity distribution for each feature
            severity_dist_true = df[true_mask]['Severity'].value_counts(normalize=True).sort_index()
            severity_dist_false = df[false_mask]['Severity'].value_counts(normalize=True).sort_index()
            
            # T-test for significance
            if true_count > 1 and false_count > 1:
                t_stat, p_value = stats.ttest_ind(
                    df[true_mask]['Severity'], 
                    df[false_mask]['Severity']
                )
            else:
                p_value = 1.0
            
            road_results.append({
                'Feature': feature,
                'Present_Count': int(true_count),
                'Present_Percentage': round(true_count / len(df) * 100, 2),
                'Severity_When_Present': round(true_severity, 4),
                'Severity_When_Absent': round(false_severity, 4),
                'Difference': round(severity_diff, 4),
                'P_Value': round(p_value, 6),
                'Significant': p_value < 0.05,
                'Severity1_Pct_Present': round(severity_dist_true.get(1, 0) * 100, 2),
                'Severity2_Pct_Present': round(severity_dist_true.get(2, 0) * 100, 2),
                'Severity3_Pct_Present': round(severity_dist_true.get(3, 0) * 100, 2),
                'Severity4_Pct_Present': round(severity_dist_true.get(4, 0) * 100, 2),
                'Severity1_Pct_Absent': round(severity_dist_false.get(1, 0) * 100, 2),
                'Severity2_Pct_Absent': round(severity_dist_false.get(2, 0) * 100, 2),
                'Severity3_Pct_Absent': round(severity_dist_false.get(3, 0) * 100, 2),
                'Severity4_Pct_Absent': round(severity_dist_false.get(4, 0) * 100, 2)
            })
            
            print(f"\n{feature}:")
            print(f"   Present in {true_count:,} accidents ({true_count/len(df)*100:.1f}%)")
            print(f"   Severity with feature: {true_severity:.3f}")
            print(f"   Severity without feature: {false_severity:.3f}")
            print(f"   Difference: {severity_diff:+.3f}")
            print(f"   Statistically significant: {'✅' if p_value < 0.05 else '❌'} (p={p_value:.4f})")
    
    # Save road features results
    road_df = pd.DataFrame(road_results)
    road_df.to_csv("outputs/tables/road_features_analysis.csv", index=False)
    print("\n✅ Saved: outputs/tables/road_features_analysis.csv")
    all_results['road_features'] = road_df
    
    # =========================================================
    # 2. GEOGRAPHIC ANALYSIS (Cities)
    # =========================================================
    print("\n" + "-" * 50)
    print("2. GEOGRAPHIC ANALYSIS - CITIES")
    print("-" * 50)
    
    # City analysis (only cities with >100 accidents for statistical significance)
    city_stats = df.groupby('City')['Severity'].agg(['mean', 'count', 'std']).reset_index()
    city_stats.columns = ['City', 'Avg_Severity', 'Accident_Count', 'Std_Dev']
    city_stats = city_stats[city_stats['Accident_Count'] >= 100].sort_values('Avg_Severity', ascending=False)
    
    # Add percentage of severe accidents (severity 3 and 4)
    severe_pct = []
    for city in city_stats['City']:
        city_df = df[df['City'] == city]
        severe_count = city_df[city_df['Severity'] >= 3].shape[0]
        severe_pct.append(round(severe_count / len(city_df) * 100, 2))
    city_stats['Severe_Accidents_Pct'] = severe_pct
    
    print("\n📊 TOP 10 MOST DANGEROUS CITIES (highest average severity):")
    print(city_stats.head(10).to_string(index=False))
    
    print("\n📊 SAFEST 10 CITIES (lowest average severity):")
    print(city_stats.tail(10).to_string(index=False))
    
    # Save city results
    city_stats.to_csv("outputs/tables/city_analysis.csv", index=False)
    print("\n✅ Saved: outputs/tables/city_analysis.csv")
    all_results['city_analysis'] = city_stats
    
    # =========================================================
    # 3. GEOGRAPHIC ANALYSIS (Counties)
    # =========================================================
    print("\n" + "-" * 50)
    print("3. GEOGRAPHIC ANALYSIS - COUNTIES")
    print("-" * 50)
    
    county_stats = df.groupby('County')['Severity'].agg(['mean', 'count', 'std']).reset_index()
    county_stats.columns = ['County', 'Avg_Severity', 'Accident_Count', 'Std_Dev']
    county_stats = county_stats[county_stats['Accident_Count'] >= 50].sort_values('Avg_Severity', ascending=False)
    
    # Add severe percentage
    severe_pct_county = []
    for county in county_stats['County']:
        county_df = df[df['County'] == county]
        severe_count = county_df[county_df['Severity'] >= 3].shape[0]
        severe_pct_county.append(round(severe_count / len(county_df) * 100, 2))
    county_stats['Severe_Accidents_Pct'] = severe_pct_county
    
    print("\n📊 TOP 10 MOST DANGEROUS COUNTIES:")
    print(county_stats.head(10).to_string(index=False))
    
    # Save county results
    county_stats.to_csv("outputs/tables/county_analysis.csv", index=False)
    print("\n✅ Saved: outputs/tables/county_analysis.csv")
    all_results['county_analysis'] = county_stats
    
    # =========================================================
    # 4. ROAD FEATURE COMBINATIONS (Multiple Risk Factors)
    # =========================================================
    print("\n" + "-" * 50)
    print("4. MULTIPLE RISK FACTORS COMBINATIONS")
    print("-" * 50)
    
    combinations = [
        {
            'name': 'Junction + No Traffic Signal + Crossing',
            'condition': (df['Junction'] == True) & (df['Traffic_Signal'] == False) & (df['Crossing'] == True)
        },
        {
            'name': 'Junction + Traffic Signal',
            'condition': (df['Junction'] == True) & (df['Traffic_Signal'] == True)
        },
        {
            'name': 'Roundabout Only (No Signal, No Junction)',
            'condition': (df['Roundabout'] == True) & (df['Traffic_Signal'] == False) & (df['Junction'] == False)
        },
        {
            'name': 'Railway Crossing + No Signal',
            'condition': (df['Railway'] == True) & (df['Traffic_Signal'] == False)
        },
        {
            'name': 'School Zone (Amenity + Crossing)',
            'condition': (df['Amenity'] == True) & (df['Crossing'] == True)
        },
        {
            'name': 'High Risk Intersection (Junction + Crossing + No Roundabout)',
            'condition': (df['Junction'] == True) & (df['Crossing'] == True) & (df['Roundabout'] == False)
        },
        {
            'name': 'Low Risk Setup (Roundabout + No Junction + No Crossing)',
            'condition': (df['Roundabout'] == True) & (df['Junction'] == False) & (df['Crossing'] == False)
        }
    ]
    
    combination_results = []
    
    for combo in combinations:
        mask = combo['condition']
        count = mask.sum()
        
        if count > 0:
            avg_severity = df[mask]['Severity'].mean()
            severe_pct = (df[mask]['Severity'] >= 3).sum() / count * 100
            
            # Compare to baseline (all accidents)
            baseline_avg = df['Severity'].mean()
            baseline_severe_pct = (df['Severity'] >= 3).sum() / len(df) * 100
            
            combination_results.append({
                'Combination': combo['name'],
                'Accident_Count': int(count),
                'Percentage_of_Total': round(count / len(df) * 100, 2),
                'Avg_Severity': round(avg_severity, 4),
                'Severe_Accidents_Pct': round(severe_pct, 2),
                'Difference_from_Baseline_Avg': round(avg_severity - baseline_avg, 4),
                'Difference_from_Baseline_Severe': round(severe_pct - baseline_severe_pct, 2)
            })
            
            print(f"\n{combo['name']}:")
            print(f"   Accidents: {count:,} ({count/len(df)*100:.1f}%)")
            print(f"   Average Severity: {avg_severity:.3f} (baseline: {baseline_avg:.3f})")
            print(f"   Severe Accidents (3+): {severe_pct:.1f}% (baseline: {baseline_severe_pct:.1f}%)")
    
    # Save combination results
    combo_df = pd.DataFrame(combination_results)
    combo_df.to_csv("outputs/tables/risk_combinations.csv", index=False)
    print("\n✅ Saved: outputs/tables/risk_combinations.csv")
    all_results['combinations'] = combo_df
    
    # =========================================================
    # 5. GA vs CT ROAD FEATURE COMPARISON
    # =========================================================
    print("\n" + "-" * 50)
    print("5. GEORGIA vs CONNECTICUT - ROAD FEATURE COMPARISON")
    print("-" * 50)
    
    ga_df = df[df['State'] == 'GA']
    ct_df = df[df['State'] == 'CT']
    
    state_comparison = []
    
    for feature in road_features:
        if feature in df.columns:
            ga_present = ga_df[feature].sum() / len(ga_df) * 100
            ct_present = ct_df[feature].sum() / len(ct_df) * 100
            
            ga_severity = ga_df[ga_df[feature] == True]['Severity'].mean()
            ct_severity = ct_df[ct_df[feature] == True]['Severity'].mean()
            
            state_comparison.append({
                'Feature': feature,
                'GA_Present_Pct': round(ga_present, 2),
                'CT_Present_Pct': round(ct_present, 2),
                'Difference_GA_CT': round(ga_present - ct_present, 2),
                'GA_Severity_When_Present': round(ga_severity, 4),
                'CT_Severity_When_Present': round(ct_severity, 4),
                'Severity_Difference': round(ga_severity - ct_severity, 4)
            })
    
    state_comparison_df = pd.DataFrame(state_comparison)
    state_comparison_df.to_csv("outputs/tables/ga_ct_road_features.csv", index=False)
    print("\n✅ Saved: outputs/tables/ga_ct_road_features.csv")
    all_results['state_comparison'] = state_comparison_df
    
    # =========================================================
    # 6. TIME + ROAD FEATURE INTERACTIONS
    # =========================================================
    print("\n" + "-" * 50)
    print("6. TIME OF DAY + ROAD FEATURE INTERACTIONS")
    print("-" * 50)
    
    time_features = ['Junction', 'Traffic_Signal', 'Crossing', 'Railway']
    time_periods = ['Morning', 'Afternoon', 'Evening', 'Night', 'Late Night']
    
    time_interaction_results = []
    
    for feature in time_features:
        for period in time_periods:
            mask = (df['TimeOfDay'] == period) & (df[feature] == True)
            count = mask.sum()
            
            if count > 100:
                avg_severity = df[mask]['Severity'].mean()
                time_interaction_results.append({
                    'Time_Period': period,
                    'Feature': feature,
                    'Accident_Count': int(count),
                    'Avg_Severity': round(avg_severity, 4)
                })
    
    time_interaction_df = pd.DataFrame(time_interaction_results)
    time_interaction_df.to_csv("outputs/tables/time_feature_interactions.csv", index=False)
    print("\n✅ Saved: outputs/tables/time_feature_interactions.csv")
    all_results['time_interactions'] = time_interaction_df
    
    # =========================================================
    # 7. WIND CHILL ANALYSIS
    # =========================================================
    print("\n" + "-" * 50)
    print("7. WIND CHILL vs TEMPERATURE ANALYSIS")
    print("-" * 50)
    
    if 'Wind_Chill(F)' in df.columns:
        # Create categories
        def get_wind_chill_category(temp):
            if pd.isna(temp):
                return 'Unknown'
            elif temp < 32:
                return 'Freezing (<32°F)'
            elif temp < 50:
                return 'Cold (32-50°F)'
            elif temp < 70:
                return 'Cool (50-70°F)'
            else:
                return 'Warm (>70°F)'
        
        df['Wind_Chill_Category'] = df['Wind_Chill(F)'].apply(get_wind_chill_category)
        
        windchill_stats = df.groupby('Wind_Chill_Category')['Severity'].agg(['mean', 'count']).reset_index()
        windchill_stats.columns = ['Category', 'Avg_Severity', 'Accident_Count']
        windchill_stats = windchill_stats[windchill_stats['Category'] != 'Unknown']
        
        print("\n📊 Severity by Wind Chill Category:")
        print(windchill_stats.to_string(index=False))
        
        windchill_stats.to_csv("outputs/tables/windchill_analysis.csv", index=False)
        print("\n✅ Saved: outputs/tables/windchill_analysis.csv")
        
        # Calculate correlation with and without wind chill
        temp_corr = df['Temperature(F)'].corr(df['Severity'])
        windchill_corr = df['Wind_Chill(F)'].corr(df['Severity'])
        
        print(f"\nTemperature correlation with severity: {temp_corr:.4f}")
        print(f"Wind Chill correlation with severity: {windchill_corr:.4f}")
        
        all_results['windchill'] = windchill_stats
    
    # =========================================================
    # 8. FINAL SUMMARY OF FINDINGS
    # =========================================================
    print("\n" + "=" * 70)
    print("📊 ADVANCED FEATURES ANALYSIS - SUMMARY")
    print("=" * 70)
    
    print("""
✅ ANALYSIS COMPLETE! The following CSV files have been created:

📁 outputs/tables/
   ├── road_features_analysis.csv       (13 road features, severity impact)
   ├── city_analysis.csv                (Cities with >100 accidents)
   ├── county_analysis.csv              (Counties with >50 accidents)
   ├── risk_combinations.csv            (Multiple risk factor combos)
   ├── ga_ct_road_features.csv          (GA vs CT comparison)
   ├── time_feature_interactions.csv    (Time + road features)
   └── windchill_analysis.csv           (Wind chill severity)

📊 KEY NUMERICAL FINDINGS READY FOR VISUALIZATION:

1. ROAD FEATURES: Which increase/decrease severity (with p-values)
2. GEOGRAPHY: Most dangerous cities and counties ranked
3. COMBINATIONS: Specific risk factor combinations to highlight
4. GA vs CT: State-by-state differences for each feature
5. TIME INTERACTIONS: How features matter differently by time of day

🎯 USE THESE CSV FILES IN visualization.py TO CREATE:
   - Bar charts of road feature impact
   - Heatmaps of risk combinations
   - Maps of dangerous cities (if you have geospatial libraries)
   - Comparison bar charts for GA vs CT
   - Line/bar charts for time-feature interactions
""")
    
    print("=" * 70)
    print("✨ ADVANCED FEATURES ANALYSIS COMPLETE! ✨")
    print("=" * 70)
    
    return all_results

if __name__ == "__main__" or __name__ == "advanced_features_analysis":
    analyze_all_features()