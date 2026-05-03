# data_cleaning.py
"""
Step 2: Clean the filtered accident data
Handles missing values, outliers, and standardizes data
"""

import pandas as pd
import numpy as np
import os

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
        cleaning_cols = ['Hour', 'Month', 'DayOfWeek', 'IsWeekend', 'TimeOfDay', 'Duration_Minutes']
        existing_cols = [col for col in cleaning_cols if col in df.columns]
        if existing_cols:
            print(f"   Cleaning features present: {', '.join(existing_cols)}")
        
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
    
    # Track cleaning statistics
    cleaning_log = {
        "initial_rows": len(df),
        "missing_handled": {},
        "outliers_removed": 0
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
    # 3. STANDARDIZE DATA
    # ============================================
    print("\n" + "-" * 40)
    print("3. STANDARDIZING DATA")
    print("-" * 40)
    
    # Create time-based features
    if 'Start_Time' in df.columns:
        # Parse dates with nanoseconds
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
        print("   ✅ Created: Duration_Minutes")
    
    # Standardize weather condition text
    if 'Weather_Condition' in df.columns:
        df['Weather_Condition'] = df['Weather_Condition'].str.upper().str.strip()
        df['Weather_Condition'] = df['Weather_Condition'].replace('', 'UNKNOWN')
        print("   ✅ Standardized weather condition text")
    
    # ============================================
    # 4. SAVE CLEANED DATA
    # ============================================
    print("\n" + "-" * 40)
    print("4. SAVING CLEANED DATA")
    print("-" * 40)
    
    df.to_csv(output_file, index=False)
    print(f"✅ Saved to: {output_file}")
    print(f"✅ Final shape: {df.shape[0]:,} rows, {df.shape[1]} columns")
    
    # ============================================
    # 5. CLEANING SUMMARY
    # ============================================
    print("\n" + "=" * 60)
    print("📊 CLEANING SUMMARY")
    print("=" * 60)
    print(f"""
Initial rows:           {cleaning_log['initial_rows']:,}
Rows after cleaning:    {len(df):,}
Rows removed:           {cleaning_log['outliers_removed']:,}
Percentage kept:        {(len(df)/cleaning_log['initial_rows'])*100:.2f}%

Missing values handled: {len(cleaning_log['missing_handled'])} columns
Outliers removed:       {cleaning_log['outliers_removed']} rows
""")
    
    print("=" * 60)
    print("✨ DATA CLEANING COMPLETE! ✨")
    print("=" * 60)
    
    return df

# This runs when the file is imported
if __name__ == "__main__" or __name__ == "data_cleaning":
    clean_data()