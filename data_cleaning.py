# data_cleaning.py
"""
Step 2: Complete Data Cleaning for US Accidents Analysis
Handles missing values, removes outliers, standardizes data
Creates ALL combination features for modeling
Saves to CSV and SQLite database
"""

import pandas as pd
import numpy as np
import os
import sqlite3

def clean_data():
    """Main function to clean the filtered accident data"""
    
    print("=" * 60)
    print("DATA CLEANING - GA & CT ACCIDENTS")
    print("=" * 60)
    
    # Define file paths using datasets folder
    input_file = os.path.join("datasets", "filtered_data.csv")
    output_file = os.path.join("datasets", "cleaned_accidents.csv")
    
    # ============================================
    # CHECK IF CLEANED DATA ALREADY EXISTS
    # ============================================
    if os.path.exists(output_file):
        print(f"\n✅ cleaned_accidents.csv already exists in datasets folder!")
        
        # Load and show summary of existing cleaned file
        df = pd.read_csv(output_file)
        print(f"   Total cleaned rows: {len(df):,}")
        print(f"   Total columns: {len(df.columns)}")
        
        # Show column names that were added during cleaning
        cleaning_cols = ['Hour', 'Month', 'DayOfWeek', 'IsWeekend', 'TimeOfDay', 
                         'Duration_Minutes', 'Rain_Junction', 'Fog_Night', 
                         'Freezing_Conditions', 'Heavy_Rain', 'Low_Visibility',
                         'Rush_Hour', 'Late_Night', 'Dangerous_Intersection', 'Safe_Road',
                         'has_blocked', 'has_jackknife', 'has_multi_vehicle', 
                         'has_rollover', 'has_road_closed', 'has_slow_traffic',
                         'has_queueing', 'has_shoulder', 'has_accident_on']
        existing_cols = [col for col in cleaning_cols if col in df.columns]
        if existing_cols:
            print(f"   Cleaning features present: {', '.join(existing_cols[:5])}...")
        
        print("\n⚠️  Skipping cleaning. Delete datasets/cleaned_accidents.csv to re-clean.")
        return df
    
    # ============================================
    # CHECK IF FILTERED DATA EXISTS
    # ============================================
    if not os.path.exists(input_file):
        print(f"\n❌ ERROR: {input_file} not found!")
        print("   Please run filter.py first to create filtered_data.csv")
        return None
    
    # Load filtered data
    print(f"\n📂 Loading {input_file}...")
    df = pd.read_csv(input_file)
    print(f"✅ Loaded {len(df):,} accidents")
    print(f"✅ Original columns: {len(df.columns)}")
    
    # Track cleaning statistics
    cleaning_log = {
        "initial_rows": len(df),
        "initial_columns": len(df.columns),
        "missing_handled": {},
        "outliers_removed": 0,
        "new_features": []
    }
    
    # ============================================
    # 1. CHECK FOR MISSING VALUES
    # ============================================
    print("\n" + "-" * 40)
    print("1. CHECKING MISSING VALUES")
    print("-" * 40)
    
    missing_before = df.isnull().sum()
    missing_before = missing_before[missing_before > 0]
    
    if len(missing_before) > 0:
        print("\nColumns with missing values BEFORE cleaning:")
        for col, count in missing_before.items():
            pct = (count / len(df)) * 100
            print(f"   {col}: {count:,} ({pct:.1f}%)")
    else:
        print("✅ No missing values found!")
    
    # Handle missing values for numerical columns
    numerical_cols = ['Temperature(F)', 'Humidity(%)', 'Pressure(in)', 
                      'Visibility(mi)', 'Wind_Speed(mph)', 'Precipitation(in)']
    
    for col in numerical_cols:
        if col in df.columns and df[col].isnull().sum() > 0:
            median_val = df[col].median()
            df[col] = df[col].fillna(median_val)
            cleaning_log["missing_handled"][col] = f"filled with median ({median_val})"
    
    # Handle missing values for categorical columns
    categorical_cols = ['Weather_Condition', 'Wind_Direction', 'Sunrise_Sunset']
    
    for col in categorical_cols:
        if col in df.columns and df[col].isnull().sum() > 0:
            mode_val = df[col].mode()[0]
            df[col] = df[col].fillna(mode_val)
            cleaning_log["missing_handled"][col] = f"filled with mode ({mode_val})"
    
    # Check after cleaning
    missing_after = df.isnull().sum().sum()
    print(f"\n✅ Missing values after cleaning: {missing_after}")
    
    # ============================================
    # 2. REMOVE OUTLIERS
    # ============================================
    print("\n" + "-" * 40)
    print("2. REMOVING OUTLIERS")
    print("-" * 40)
    
    initial_count = len(df)
    
    # Remove unrealistic temperatures
    if 'Temperature(F)' in df.columns:
        temp_outliers = df[(df['Temperature(F)'] < -50) | (df['Temperature(F)'] > 130)]
        df = df[(df['Temperature(F)'] >= -50) & (df['Temperature(F)'] <= 130)]
        print(f"   Temperature outliers removed: {len(temp_outliers)}")
    
    # Remove unrealistic humidity
    if 'Humidity(%)' in df.columns:
        humidity_outliers = df[(df['Humidity(%)'] < 0) | (df['Humidity(%)'] > 100)]
        df = df[(df['Humidity(%)'] >= 0) & (df['Humidity(%)'] <= 100)]
        print(f"   Humidity outliers removed: {len(humidity_outliers)}")
    
    # Remove unrealistic visibility
    if 'Visibility(mi)' in df.columns:
        visibility_outliers = df[df['Visibility(mi)'] < 0]
        df = df[df['Visibility(mi)'] >= 0]
        print(f"   Visibility outliers removed: {len(visibility_outliers)}")
    
    cleaning_log["outliers_removed"] = initial_count - len(df)
    print(f"\n✅ Total rows removed: {cleaning_log['outliers_removed']}")
    print(f"✅ Final row count: {len(df):,}")
    
    # ============================================
    # 3. STANDARDIZE DATA AND CREATE TIME FEATURES
    # ============================================
    print("\n" + "-" * 40)
    print("3. STANDARDIZING DATA & CREATING TIME FEATURES")
    print("-" * 40)
    
    # Create time-based features
    if 'Start_Time' in df.columns:
        try:
            df['Start_Time'] = pd.to_datetime(df['Start_Time'], format='mixed')
            print("   ✅ Parsed dates with mixed format")
        except:
            try:
                df['Start_Time'] = df['Start_Time'].str.split('.').str[0]
                df['Start_Time'] = pd.to_datetime(df['Start_Time'])
                print("   ✅ Parsed dates by removing nanoseconds")
            except:
                df['Start_Time'] = pd.to_datetime(df['Start_Time'], format='ISO8601')
                print("   ✅ Parsed dates with ISO8601 format")
        
        df['Hour'] = df['Start_Time'].dt.hour
        df['Month'] = df['Start_Time'].dt.month
        df['DayOfWeek'] = df['Start_Time'].dt.dayofweek
        df['IsWeekend'] = df['DayOfWeek'].isin([5, 6]).astype(int)
        
        def get_time_category(hour):
            if 6 <= hour < 12:
                return 'Morning'
            elif 12 <= hour < 17:
                return 'Afternoon'
            elif 17 <= hour < 20:
                return 'Evening'
            elif 20 <= hour < 24:
                return 'Night'
            else:
                return 'Late Night'
        
        df['TimeOfDay'] = df['Hour'].apply(get_time_category)
        cleaning_log["new_features"].extend(['Hour', 'Month', 'DayOfWeek', 'IsWeekend', 'TimeOfDay'])
        print("   ✅ Created: Hour, Month, DayOfWeek, IsWeekend, TimeOfDay")
    
    # Parse End_Time and calculate duration
    if 'End_Time' in df.columns:
        try:
            df['End_Time'] = pd.to_datetime(df['End_Time'], format='mixed')
            print("   ✅ Parsed End_Time dates")
        except:
            try:
                df['End_Time'] = df['End_Time'].str.split('.').str[0]
                df['End_Time'] = pd.to_datetime(df['End_Time'])
                print("   ✅ Parsed End_Time dates by removing nanoseconds")
            except:
                df['End_Time'] = pd.to_datetime(df['End_Time'], format='ISO8601')
                print("   ✅ Parsed End_Time dates with ISO8601 format")
        
        df['Duration_Minutes'] = (df['End_Time'] - df['Start_Time']).dt.total_seconds() / 60
        cleaning_log["new_features"].append('Duration_Minutes')
        print("   ✅ Created: Duration_Minutes")
    
    # Standardize weather condition text
    if 'Weather_Condition' in df.columns:
        df['Weather_Condition'] = df['Weather_Condition'].str.upper().str.strip()
        df['Weather_Condition'] = df['Weather_Condition'].replace('', 'UNKNOWN')
        print("   ✅ Standardized weather condition text")
    
    # ============================================
    # 4. CREATE WEATHER COMBINATION FEATURES
    # ============================================
    print("\n" + "-" * 40)
    print("4. CREATING WEATHER COMBINATION FEATURES")
    print("-" * 40)
    
    # Rain + Junction
    if 'Weather_Condition' in df.columns and 'Junction' in df.columns:
        df['Rain_Junction'] = ((df['Weather_Condition'].str.contains('RAIN', na=False)) & (df['Junction'] == True)).astype(int)
        cleaning_log["new_features"].append('Rain_Junction')
        print("   ✅ Created: Rain_Junction (rain at intersection)")
    
    # Fog + Night
    if 'Weather_Condition' in df.columns and 'Sunrise_Sunset' in df.columns:
        df['Fog_Night'] = ((df['Weather_Condition'].str.contains('FOG', na=False)) & (df['Sunrise_Sunset'] == 'Night')).astype(int)
        cleaning_log["new_features"].append('Fog_Night')
        print("   ✅ Created: Fog_Night (fog at night)")
    
    # Freezing conditions (cold + humid)
    if 'Temperature(F)' in df.columns and 'Humidity(%)' in df.columns:
        df['Freezing_Conditions'] = ((df['Temperature(F)'] < 35) & (df['Humidity(%)'] > 80)).astype(int)
        cleaning_log["new_features"].append('Freezing_Conditions')
        print("   ✅ Created: Freezing_Conditions (below freezing + high humidity)")
    
    # Heavy rain
    if 'Precipitation(in)' in df.columns:
        df['Heavy_Rain'] = (df['Precipitation(in)'] > 0.2).astype(int)
        cleaning_log["new_features"].append('Heavy_Rain')
        print("   ✅ Created: Heavy_Rain (>0.2 inches)")
    
    # Low visibility
    if 'Visibility(mi)' in df.columns:
        df['Low_Visibility'] = (df['Visibility(mi)'] < 1).astype(int)
        cleaning_log["new_features"].append('Low_Visibility')
        print("   ✅ Created: Low_Visibility (<1 mile)")
    
    # ============================================
    # 5. CREATE TIME COMBINATION FEATURES
    # ============================================
    print("\n" + "-" * 40)
    print("5. CREATING TIME COMBINATION FEATURES")
    print("-" * 40)
    
    if 'Hour' in df.columns:
        # Rush hour (7-9 AM and 4-6 PM)
        df['Rush_Hour'] = ((df['Hour'].between(7, 9)) | (df['Hour'].between(16, 18))).astype(int)
        cleaning_log["new_features"].append('Rush_Hour')
        print("   ✅ Created: Rush_Hour (7-9 AM or 4-6 PM)")
        
        # Late night (12-5 AM)
        df['Late_Night'] = (df['Hour'].between(0, 5)).astype(int)
        cleaning_log["new_features"].append('Late_Night')
        print("   ✅ Created: Late_Night (12-5 AM)")
    
    # ============================================
    # 6. CREATE ROAD FEATURE COMBINATIONS
    # ============================================
    print("\n" + "-" * 40)
    print("6. CREATING ROAD FEATURE COMBINATIONS")
    print("-" * 40)
    
    # Dangerous intersection (Junction + no roundabout + no signal)
    if 'Junction' in df.columns and 'Roundabout' in df.columns and 'Traffic_Signal' in df.columns:
        df['Dangerous_Intersection'] = ((df['Junction'] == True) & 
                                         (df['Roundabout'] == False) & 
                                         (df['Traffic_Signal'] == False)).astype(int)
        cleaning_log["new_features"].append('Dangerous_Intersection')
        print("   ✅ Created: Dangerous_Intersection (junction without roundabout or signal)")
    
    # Safe road (traffic calming or roundabout)
    if 'Traffic_Calming' in df.columns and 'Roundabout' in df.columns:
        df['Safe_Road'] = ((df['Traffic_Calming'] == True) | (df['Roundabout'] == True)).astype(int)
        cleaning_log["new_features"].append('Safe_Road')
        print("   ✅ Created: Safe_Road (has traffic calming or roundabout)")
    
    # ============================================
    # 7. EXTRACT TEXT KEYWORDS FROM DESCRIPTION
    # ============================================
    print("\n" + "-" * 40)
    print("7. EXTRACTING TEXT KEYWORDS FROM DESCRIPTION")
    print("-" * 40)
    
    if 'Description' in df.columns:
        # High severity keywords
        df['has_blocked'] = df['Description'].str.contains('blocked', case=False, na=False).astype(int)
        df['has_jackknife'] = df['Description'].str.contains('jackknife', case=False, na=False).astype(int)
        df['has_multi_vehicle'] = df['Description'].str.contains('multi-vehicle|multi vehicle', case=False, na=False).astype(int)
        df['has_rollover'] = df['Description'].str.contains('rollover', case=False, na=False).astype(int)
        df['has_road_closed'] = df['Description'].str.contains('road closed', case=False, na=False).astype(int)
        
        # Medium severity keywords
        df['has_slow_traffic'] = df['Description'].str.contains('slow traffic', case=False, na=False).astype(int)
        df['has_queueing'] = df['Description'].str.contains('queueing', case=False, na=False).astype(int)
        df['has_shoulder'] = df['Description'].str.contains('shoulder', case=False, na=False).astype(int)
        
        # Low severity keywords
        df['has_accident_on'] = df['Description'].str.contains('accident on', case=False, na=False).astype(int)
        
        cleaning_log["new_features"].extend([
            'has_blocked', 'has_jackknife', 'has_multi_vehicle', 'has_rollover',
            'has_road_closed', 'has_slow_traffic', 'has_queueing', 'has_shoulder', 'has_accident_on'
        ])
        print("   ✅ Created text keyword features:")
        print("      - has_blocked (lanes blocked)")
        print("      - has_jackknife (truck accident)")
        print("      - has_multi_vehicle (multiple cars)")
        print("      - has_rollover (vehicle flipped)")
        print("      - has_road_closed (complete closure)")
        print("      - has_slow_traffic (traffic slowing)")
        print("      - has_queueing (traffic backing up)")
        print("      - has_shoulder (shoulder affected)")
        print("      - has_accident_on (generic accident)")
    
    # ============================================
    # 8. REMOVE USELESS COLUMNS
    # ============================================
    print("\n" + "-" * 40)
    print("8. REMOVING USELESS COLUMNS")
    print("-" * 40)
    
    # Columns to KEEP (all useful ones)
    useful_columns = [
        # Target
        'Severity',
        
        # Location
        'State', 'City', 'County',
        
        # Weather (original)
        'Temperature(F)', 'Humidity(%)', 'Precipitation(in)', 
        'Visibility(mi)', 'Wind_Speed(mph)', 'Weather_Condition',
        
        # Time (original)
        'Hour', 'Month', 'DayOfWeek', 'IsWeekend', 'TimeOfDay', 'Sunrise_Sunset',
        
        # Duration
        'Duration_Minutes',
        
        # Road features (original)
        'Junction', 'Traffic_Signal', 'Crossing', 'Railway', 'Stop',
        'Traffic_Calming', 'Roundabout', 'Amenity', 'Station', 'No_Exit',
        
        # Description (for text analysis)
        'Description',
        
        # Coordinates (for mapping)
        'Start_Lat', 'Start_Lng',
        
        # WEATHER COMBINATIONS
        'Rain_Junction', 'Fog_Night', 'Freezing_Conditions', 'Heavy_Rain', 'Low_Visibility',
        
        # TIME COMBINATIONS
        'Rush_Hour', 'Late_Night',
        
        # ROAD COMBINATIONS
        'Dangerous_Intersection', 'Safe_Road',
        
        # TEXT KEYWORDS
        'has_blocked', 'has_jackknife', 'has_multi_vehicle', 'has_rollover',
        'has_road_closed', 'has_slow_traffic', 'has_queueing', 'has_shoulder', 'has_accident_on'
    ]
    
    # Keep only columns that exist
    existing_columns = [col for col in useful_columns if col in df.columns]
    removed_count = len(df.columns) - len(existing_columns)
    df = df[existing_columns]
    
    print(f"   ✅ Kept {len(existing_columns)} useful columns")
    print(f"   ✅ Removed {removed_count} useless columns")
    
    # ============================================
    # 9. SAVE CLEANED DATA AS CSV AND SQLITE
    # ============================================
    print("\n" + "-" * 40)
    print("9. SAVING CLEANED DATA")
    print("-" * 40)
    
    # Save to CSV
    df.to_csv(output_file, index=False)
    print(f"✅ Saved cleaned data to CSV: {output_file}")
    
    # Save to SQLite DB
    db_file = os.path.join("datasets", "cleaned_accidents.db")
    conn = sqlite3.connect(db_file)
    df.to_sql("cleaned_accidents", conn, if_exists="replace", index=False)
    conn.close()
    print(f"✅ Saved cleaned data to database: {db_file}")
    print(f"   📊 Table name: cleaned_accidents")
    print(f"   📊 Final shape: {df.shape[0]:,} rows, {df.shape[1]} columns")
    
    # ============================================
    # 10. CLEANING SUMMARY
    # ============================================
    print("\n" + "=" * 60)
    print("📊 CLEANING SUMMARY")
    print("=" * 60)
    
    print(f"""
Initial rows:           {cleaning_log['initial_rows']:,}
Final rows:             {len(df):,}
Rows removed:           {cleaning_log['outliers_removed']:,}
Percentage kept:        {(len(df)/cleaning_log['initial_rows'])*100:.2f}%

Initial columns:        {cleaning_log['initial_columns']}
Final columns:          {len(df.columns)}

NEW FEATURES CREATED ({len(cleaning_log['new_features'])} total):
   Time features: Hour, Month, DayOfWeek, IsWeekend, TimeOfDay, Duration_Minutes
   Weather combos: Rain_Junction, Fog_Night, Freezing_Conditions, Heavy_Rain, Low_Visibility
   Time combos: Rush_Hour, Late_Night
   Road combos: Dangerous_Intersection, Safe_Road
   Text keywords: has_blocked, has_jackknife, has_multi_vehicle, has_rollover,
                  has_road_closed, has_slow_traffic, has_queueing, has_shoulder, has_accident_on

Missing values handled: {len(cleaning_log['missing_handled'])} columns
Outliers removed:       {cleaning_log['outliers_removed']} rows
""")
    
    print("=" * 60)
    print("✨ DATA CLEANING COMPLETE! ✨")
    print("=" * 60)
    
    return df

if __name__ == "__main__" or __name__ == "data_cleaning":
    clean_data()