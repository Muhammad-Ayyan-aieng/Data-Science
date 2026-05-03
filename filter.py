"""
Filter US Accidents Data for GA and CT
Extracts only Georgia and Connecticut accident records
"""

import pandas as pd
import time
import os

def filter_data():
    """Main function to filter GA and CT data from the large CSV file"""
    
    print("=" * 60)
    print("FILTERING US ACCIDENTS DATA FOR GA & CT")
    print("=" * 60)
    
    # Define file paths using datasets folder
    input_file = os.path.join("datasets", "US_Accidents_March23.csv")    
    output_file = os.path.join("datasets", "filtered_data.csv")
    os.makedirs("datasets", exist_ok=True)
    
    # Check if already filtered
    if os.path.exists(output_file):
        print("\n✅ filtered_data.csv already exists in datasets folder!")
        
        # Show summary of existing file
        df = pd.read_csv(output_file)
        print(f"   Total GA & CT rows: {len(df):,}")
        print(df["State"].value_counts().to_string())
        print("\n⚠️  Skipping filtering. Delete the file to re-filter.")
        return df
    
    # Check if input file exists
    if not os.path.exists(input_file):
        print(f"\n❌ ERROR: {input_file} not found!")
        print("   Please make sure the file is in the 'datasets' folder.")
        return None
    
    start_time = time.time()
    chunk_size = 100000
    filtered_chunks = []
    total_rows = 0
    total_filtered = 0
    
    print(f"\n📂 Reading file in chunks of {chunk_size:,} rows...\n")
    
    for i, chunk in enumerate(pd.read_csv(input_file, chunksize=chunk_size)):
        
        total_rows += len(chunk)
        filtered_chunk = chunk[chunk["State"].isin(["GA", "CT"])]
        total_filtered += len(filtered_chunk)
        
        if len(filtered_chunk) > 0:
            filtered_chunks.append(filtered_chunk)
        
        # Show progress every 10 chunks
        if (i + 1) % 10 == 0:
            print(f"Chunk {i+1}: Processed {total_rows:,} rows | Found {total_filtered:,} GA/CT rows | {((total_rows/7728394)*100):.1f}% complete")
    
    print("\n" + "=" * 60)
    print("📊 FILTERING COMPLETE!")
    print("=" * 60)
    
    if filtered_chunks:
        final_df = pd.concat(filtered_chunks, ignore_index=True)
        
        print(f"\n✅ Total rows in original file: {total_rows:,}")
        print(f"✅ Total GA & CT rows: {len(final_df):,}")
        print(f"✅ Percentage kept: {(len(final_df)/total_rows)*100:.2f}%")
        
        print(f"\n💾 Saving to '{output_file}'...")
        final_df.to_csv(output_file, index=False)
        
        print("\n📊 State breakdown:")
        print(final_df["State"].value_counts())
        
        elapsed_time = (time.time() - start_time) / 60
        print(f"\n⏱️  Time taken: {elapsed_time:.2f} minutes")
        print(f"✅ Saved successfully! File: {output_file}")
        
        return final_df
    else:
        print("❌ No GA or CT data found!")
        return None

# This runs when the file is imported
if __name__ == "__main__" or __name__ == "filter":
    filter_data()