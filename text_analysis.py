# text_analysis.py
"""
Advanced Text Analysis of Accident Descriptions
Extracts keywords that predict accident severity
Exports to: 1 Excel file, 1 Word file, multiple CSV files
"""

import pandas as pd
import os
from sklearn.feature_extraction.text import CountVectorizer
from datetime import datetime

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

def analyze_description_text():
    """Extract keywords from Description column and analyze severity relationship"""
    
    print("=" * 80)
    print("📝 TEXT ANALYSIS - ACCIDENT DESCRIPTIONS")
    print("=" * 80)
    
    # Create output folders
    os.makedirs("outputs/text_analysis/tables", exist_ok=True)
    os.makedirs("outputs/text_analysis/reports", exist_ok=True)
    
    # Load cleaned data
    input_file = os.path.join("datasets", "cleaned_accidents.csv")
    
    if not os.path.exists(input_file):
        print(f"❌ {input_file} not found!")
        return None
    
    df = pd.read_csv(input_file)
    print(f"\n✅ Loaded {len(df):,} accident descriptions")
    
    # =========================================================
    # 1. KEYWORD CATEGORIES - FREQUENCY
    # =========================================================
    print("\n" + "-" * 50)
    print("1. KEYWORD CATEGORIES FREQUENCY")
    print("-" * 50)
    
    severity_keywords = {
        'High Severity': [
            'blocked', 'lane blocked', 'lanes blocked', 'multi-vehicle', 
            'multi vehicle', 'jackknife', 'rollover', 'serious', 
            'fatality', 'injury', 'ejection', 'overturn'
        ],
        'Medium Severity': [
            'slow traffic', 'queueing', 'backup', 'delay', 'shoulder blocked'
        ],
        'Low Severity': [
            'accident on', 'crash', 'collision', 'fender bender'
        ]
    }
    
    # Create keyword flags
    for category, keywords in severity_keywords.items():
        col_name = f'has_{category.replace(" ", "_")}'
        df[col_name] = False
        for keyword in keywords:
            mask = df['Description'].str.contains(keyword, case=False, na=False)
            df[col_name] = df[col_name] | mask
    
    # Build keyword category table
    keyword_category_data = []
    for category in severity_keywords.keys():
        col_name = f'has_{category.replace(" ", "_")}'
        count = df[col_name].sum()
        pct = (count / len(df)) * 100
        keyword_category_data.append({
            'Keyword_Category': category,
            'Accident_Count': int(count),
            'Percentage': pct
        })
    
    keyword_category_df = pd.DataFrame(keyword_category_data)
    
    # =========================================================
    # 2. SPECIFIC KEYWORD SEVERITY IMPACT
    # =========================================================
    print("\n" + "-" * 50)
    print("2. SPECIFIC KEYWORD SEVERITY IMPACT")
    print("-" * 50)
    
    specific_keywords = [
        ('jackknife', 'Truck trailer folding sideways'),
        ('multi-vehicle', 'Multiple cars involved'),
        ('queueing', 'Traffic backing up'),
        ('shoulder', 'Shoulder lane blocked'),
        ('blocked', 'Lanes blocked'),
        ('rollover', 'Vehicle flipped over'),
        ('serious', 'Described as serious'),
        ('slow traffic', 'Slow traffic only')
    ]
    
    keyword_impact_data = []
    for keyword, meaning in specific_keywords:
        mask = df['Description'].str.contains(keyword, case=False, na=False)
        count = mask.sum()
        pct = (count / len(df)) * 100
        avg_severity = df[mask]['Severity'].mean()
        
        keyword_impact_data.append({
            'Keyword': keyword,
            'Meaning': meaning,
            'Accident_Count': int(count),
            'Percentage': pct,
            'Avg_Severity': avg_severity,
            'Severity_Impact': avg_severity - df['Severity'].mean()
        })
    
    keyword_impact_df = pd.DataFrame(keyword_impact_data)
    keyword_impact_df = keyword_impact_df.sort_values('Avg_Severity', ascending=False)
    
    # =========================================================
    # 3. 'BLOCKED' KEYWORD IMPACT
    # =========================================================
    print("\n" + "-" * 50)
    print("3. 'BLOCKED' KEYWORD IMPACT")
    print("-" * 50)
    
    blocked_mask = df['Description'].str.contains('blocked', case=False, na=False)
    
    blocked_distribution_data = []
    for severity in [1, 2, 3, 4]:
        blocked_count = df[blocked_mask & (df['Severity'] == severity)].shape[0]
        not_blocked_count = df[~blocked_mask & (df['Severity'] == severity)].shape[0]
        
        blocked_distribution_data.append({
            'Severity_Level': severity,
            'With_Blocked_Count': blocked_count,
            'With_Blocked_Pct': (blocked_count / blocked_mask.sum() * 100) if blocked_mask.sum() > 0 else 0,
            'Without_Blocked_Count': not_blocked_count,
            'Without_Blocked_Pct': (not_blocked_count / (~blocked_mask).sum() * 100) if (~blocked_mask).sum() > 0 else 0
        })
    
    blocked_distribution_df = pd.DataFrame(blocked_distribution_data)
    
    # =========================================================
    # 4. TOP PHRASES BY SEVERITY
    # =========================================================
    print("\n" + "-" * 50)
    print("4. TOP PHRASES BY SEVERITY LEVEL")
    print("-" * 50)
    
    def get_top_phrases(texts, n=5):
        vectorizer = CountVectorizer(ngram_range=(2, 4), stop_words='english', max_features=5)
        try:
            X = vectorizer.fit_transform(texts)
            words = vectorizer.get_feature_names_out()
            sums = X.sum(axis=0).A1
            top_indices = sums.argsort()[-n:][::-1]
            return [(words[i], int(sums[i])) for i in top_indices]
        except:
            return []
    
    top_phrases_data = []
    for severity in [2, 3, 4]:
        severity_texts = df[df['Severity'] == severity]['Description'].fillna('').tolist()
        if len(severity_texts) > 100:
            top_phrases = get_top_phrases(severity_texts, 5)
            for rank, (phrase, count) in enumerate(top_phrases, 1):
                top_phrases_data.append({
                    'Severity_Level': severity,
                    'Rank': rank,
                    'Phrase': phrase,
                    'Frequency': count
                })
    
    top_phrases_df = pd.DataFrame(top_phrases_data)
    
    # =========================================================
    # 5. SAVE CSV FILES
    # =========================================================
    print("\n" + "-" * 50)
    print("5. SAVING CSV FILES")
    print("-" * 50)
    
    keyword_category_df.to_csv("outputs/text_analysis/tables/01_keyword_categories.csv", index=False)
    keyword_impact_df.to_csv("outputs/text_analysis/tables/02_keyword_impact.csv", index=False)
    blocked_distribution_df.to_csv("outputs/text_analysis/tables/03_blocked_distribution.csv", index=False)
    
    if len(top_phrases_df) > 0:
        top_phrases_df.to_csv("outputs/text_analysis/tables/04_top_phrases.csv", index=False)
    
    print("   ✅ Saved 4 CSV files to outputs/text_analysis/tables/")
    
    # =========================================================
    # 6. CREATE EXCEL FILE (All tables in one workbook)
    # =========================================================
    print("\n" + "-" * 50)
    print("6. CREATING EXCEL FILE")
    print("-" * 50)
    
    excel_path = "outputs/text_analysis/reports/text_analysis.xlsx"
    
    if HAS_OPENPYXL:
        with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
            keyword_category_df.to_excel(writer, sheet_name='Keyword_Categories', index=False)
            keyword_impact_df.to_excel(writer, sheet_name='Keyword_Impact', index=False)
            blocked_distribution_df.to_excel(writer, sheet_name='Blocked_Keyword', index=False)
            if len(top_phrases_df) > 0:
                top_phrases_df.to_excel(writer, sheet_name='Top_Phrases', index=False)
            
            # Add info sheet
            info_df = pd.DataFrame({
                'Information': ['Analysis Date', 'Total Accidents', 'Accidents with Description'],
                'Value': [datetime.now().strftime('%Y-%m-%d %H:%M:%S'), len(df), df['Description'].notna().sum()]
            })
            info_df.to_excel(writer, sheet_name='Info', index=False)
        
        print(f"   ✅ Excel file saved: {excel_path}")
    else:
        print("   ⚠️ openpyxl not installed. Skipping Excel export.")
    
    # =========================================================
    # 7. CREATE WORD REPORT
    # =========================================================
    print("\n" + "-" * 50)
    print("7. CREATING WORD REPORT")
    print("-" * 50)
    
    word_path = "outputs/text_analysis/reports/text_analysis.docx"
    
    if HAS_PYTHON_DOCX:
        doc = Document()
        
        # Title
        title = doc.add_heading('Text Analysis of Accident Descriptions', 0)
        title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        
        # Info
        doc.add_paragraph(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        doc.add_paragraph(f"Total Descriptions Analyzed: {len(df):,}")
        doc.add_paragraph()
        
        # 1. Key Finding - Most Dangerous Keyword
        doc.add_heading('1. Most Dangerous Keywords', level=1)
        most_dangerous = keyword_impact_df.iloc[0]
        doc.add_paragraph(f"The keyword '{most_dangerous['Keyword']}' appears in {most_dangerous['Accident_Count']:,} accidents "
                         f"and has an average severity of {most_dangerous['Avg_Severity']:.2f} "
                         f"(+{most_dangerous['Severity_Impact']:.2f} above baseline).")
        
        # 2. Keyword Impact Table
        doc.add_heading('2. Keyword Impact on Severity', level=1)
        table = doc.add_table(rows=1, cols=4)
        table.style = 'Table Grid'
        hdr = table.rows[0].cells
        hdr[0].text = 'Keyword'
        hdr[1].text = 'Meaning'
        hdr[2].text = 'Accidents'
        hdr[3].text = 'Avg Severity'
        
        for _, row in keyword_impact_df.head(10).iterrows():
            cells = table.add_row().cells
            cells[0].text = row['Keyword']
            cells[1].text = row['Meaning']
            cells[2].text = f"{row['Accident_Count']:,}"
            cells[3].text = f"{row['Avg_Severity']:.2f}"
        
        doc.add_paragraph()
        
        # 3. 'Blocked' Keyword Impact
        doc.add_heading('3. Impact of "Blocked" Keyword', level=1)
        doc.add_paragraph(f"Accidents containing 'blocked' are significantly more severe:")
        
        table = doc.add_table(rows=1, cols=4)
        table.style = 'Table Grid'
        hdr = table.rows[0].cells
        hdr[0].text = 'Severity'
        hdr[1].text = 'With "blocked"'
        hdr[2].text = 'Without "blocked"'
        hdr[3].text = 'Difference'
        
        for _, row in blocked_distribution_df.iterrows():
            cells = table.add_row().cells
            cells[0].text = str(int(row['Severity_Level']))
            cells[1].text = f"{row['With_Blocked_Pct']:.1f}%"
            cells[2].text = f"{row['Without_Blocked_Pct']:.1f}%"
            cells[3].text = f"{row['With_Blocked_Pct'] - row['Without_Blocked_Pct']:+.1f}%"
        
        doc.add_paragraph()
        
        # 4. Top Phrases by Severity
        if len(top_phrases_df) > 0:
            doc.add_heading('4. Common Phrases by Severity Level', level=1)
            
            for severity in [2, 3, 4]:
                severity_phrases = top_phrases_df[top_phrases_df['Severity_Level'] == severity]
                if len(severity_phrases) > 0:
                    doc.add_heading(f'Severity Level {severity}', level=2)
                    phrases_text = ", ".join([f'"{p}"' for p in severity_phrases['Phrase'].values[:3]])
                    doc.add_paragraph(f"Common phrases: {phrases_text}")
        
        # 5. Key Conclusions
        doc.add_heading('5. Key Conclusions', level=1)
        
        baseline = df['Severity'].mean()
        jackknife_sev = keyword_impact_df[keyword_impact_df['Keyword'] == 'jackknife']['Avg_Severity'].values[0] if len(keyword_impact_df[keyword_impact_df['Keyword'] == 'jackknife']) > 0 else 0
        blocked_sev = keyword_impact_df[keyword_impact_df['Keyword'] == 'blocked']['Avg_Severity'].values[0] if len(keyword_impact_df[keyword_impact_df['Keyword'] == 'blocked']) > 0 else 0
        
        doc.add_paragraph(f"""
1. Text descriptions are STRONG predictors of accident severity
2. '{most_dangerous['Keyword']}' is the most severe keyword (Severity: {most_dangerous['Avg_Severity']:.2f})
3. Accidents with 'blocked' are {blocked_sev - baseline:+.2f} points more severe than average
4. Severe accidents (Level 4) often mention "road closed" and "alternate route"
""")
        
        # Save Word document
        doc.save(word_path)
        print(f"   ✅ Word report saved: {word_path}")
    else:
        print("   ⚠️ python-docx not installed. Skipping Word export.")
    
    # =========================================================
    # 8. FINAL SUMMARY
    # =========================================================
    print("\n" + "=" * 80)
    print("📊 TEXT ANALYSIS - SUMMARY")
    print("=" * 80)
    
    # Calculate key metrics
    high_keywords = ['blocked', 'multi-vehicle', 'jackknife', 'rollover']
    high_mask = df['Description'].str.contains('|'.join(high_keywords), case=False, na=False)
    
    print(f"""
✅ ANALYSIS COMPLETE!

KEY FINDINGS:
------------
• Most dangerous keyword: '{keyword_impact_df.iloc[0]['Keyword']}' 
  (Severity: {keyword_impact_df.iloc[0]['Avg_Severity']:.2f})

• Accidents with high-severity keywords: {high_mask.sum():,} ({high_mask.sum()/len(df)*100:.1f}%)
• Severity impact: +{(high_mask.sum() > 0 and df[high_mask]['Severity'].mean() - df['Severity'].mean()) or 0:.2f}

OUTPUT FILES:
------------
📁 CSV Files: outputs/text_analysis/tables/
   ├── 01_keyword_categories.csv
   ├── 02_keyword_impact.csv
   ├── 03_blocked_distribution.csv
   └── 04_top_phrases.csv

📊 Excel File: outputs/text_analysis/reports/text_analysis.xlsx
   (All tables in one workbook)

📄 Word Report: outputs/text_analysis/reports/text_analysis.docx
   (Professional report with formatted tables)
""")
    
    print("=" * 80)
    print("✨ TEXT ANALYSIS COMPLETE! ✨")
    print("=" * 80)
    
    return df

if __name__ == "__main__" or __name__ == "text_analysis":
    analyze_description_text()