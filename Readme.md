# Accidents Analysis: Georgia vs Connecticut

**Course:** AINE 312 - Data Science | **Term:** Spring 2025/26 | **States:** GA & CT

## Dataset Source

**Original Dataset:** [US Accidents (2016 - 2023)](https://www.kaggle.com/datasets/sobhanmoosavi/us-accidents) by Sobhan Moosavi

| Property      |    Value    |
|---------------|-------------|
| Total Records |  7,728,394  |
| Time Period   | 2016 - 2023 |
| File Size     |    3.06 GB  |

## Complete Processing Pipeline
Step 1: Filter.py → 7.7M rows → 240,239 rows (GA & CT only)
Step 2: Data Cleaning → 240,239 rows → 240,225 rows (cleaned)
Step 3: Statistics → Mean, Median, Std, Correlations
Step 4: Text Analysis → Keywords, Phrases, Severity impact
Step 5: Advanced Features → Road features, Cities, Counties
Step 6: Visualization → 13 professional charts

## Step-by-Step Procedure

### Step 1: Filter Data (`filter.py`)

**What it does:** Extracts only Georgia and Connecticut accidents from 7.7 million records

**Input:** `datasets/US_Accidents_March23.csv` (7.7M rows)

**Process:** Reads file in chunks of 100,000 rows, keeps only State = GA or CT

**Output:** `datasets/filtered_data.csv` (240,239 rows)

| State |  Count  |
|-------|---------|
|  GA   | 169,234 |
|  CT   |  71,005 |

### Step 2: Clean Data (`data_cleaning.py`)

**What it does:** Handles missing values, removes outliers, standardizes data

**Input:** `datasets/filtered_data.csv`

**Process:**
- Fill missing numerical values with MEDIAN
- Fill missing categorical values with MODE
- Remove temperature outliers (< -50°F or > 130°F)
- Remove humidity outliers (< 0% or > 100%)
- Convert dates and extract Hour, Month, DayOfWeek
- Calculate accident duration in minutes

**Output:** `datasets/cleaned_accidents.csv` (240,225 rows, 52 columns)

|    Metric    | Value  |
|--------------|--------|
| Rows removed | 14     |
| Final rows   | 240,225|
| Final columns| 52     |

### Step 3: Statistical Analysis (`statistical_analysis.py`)

**What it does:** Calculates mean, median, standard deviation, correlations, distributions

**Input:** `datasets/cleaned_accidents.csv`

**Outputs (11 CSV files):**

|             File              |                  Contents                   |
|-------------------------------|---------------------------------------------|
| `numerical_statistics.csv`    | Mean, median, std for all numerical features|
| `severity_distribution.csv`   | Count and % for each severity level         |
| `severity_correlations.csv`   | Correlation with severity                   | 
| `time_of_day_distribution.csv`| Accidents by time period                    |
| `state_distribution.csv`      | GA vs CT counts                             |
| `ga_vs_ct_comparison.csv`     | Full state comparison                       |
| And 5 more... | |

**Key Results:**

| Severity | Count  | Percentage |
|----------|--------|------------|
|     1    | 1,079  | 0.45%      |
|     2    | 144,588| 60.19%     |
|     3    | 77,613 | 32.31%     |
|     4    | 16,945 | 7.05%      |

|    Time Period     | Percentage |
|--------------------|------------|
| Morning (6-12 PM)  |   34.8%    |
| Afternoon (12-5 PM)|   29.0%    |
| Evening (5-8 PM)   |   16.9%    |

### Step 4: Text Analysis (`text_analysis.py`)

**What it does:** Extracts keywords from accident descriptions to predict severity

**Input:** `datasets/cleaned_accidents.csv`

**Process:**
- Define high/medium/low severity keywords
- Search for keywords in Description column
- Calculate average severity for each keyword
- Find most common phrases by severity level

**Outputs (7 CSV files):**

|                File                |                  Contents                    |
|------------------------------------|----------------------------------------------|
| `keyword_counts.csv`               | How many accidents contain each keyword type |
| `specific_keyword_analysis.csv`    | Severity score for each keyword              | 
| `blocked_keyword_distribution.csv` | Severity distribution with/without 'blocked' |
| `top_phrases_by_severity.csv`      | Most common phrases for severity 2,3,4       |
| And 3 more... | |

**Key Results:**

|   Keyword   |    Avg Severity    |
|-------------|--------------------|
| jackknife   | **3.09** (Highest) |
| blocked     | 2.65               |
| slow traffic| 2.13 (Lowest)      |

| Severity |             Top Phrases                |
|----------|----------------------------------------|
|    2     | lane blocked, slow traffic, right lane |
|    3     | blocked accident, lane blocked         |
|    4     | road closed, alternate route           |

---

### Step 5: Advanced Features (`advanced_features_analysis.py`)

**What it does:** Analyzes road features, cities, counties, and risk combinations

**Input:** `datasets/cleaned_accidents.csv`

**Outputs (7 CSV files):**

|           File              |              Contents                   |
|-----------------------------|-----------------------------------------|
| `road_features_analysis.csv`| Impact of each road feature on severity |
| `city_analysis.csv`         | Most dangerous and safest cities        |
| `county_analysis.csv`       | County-level severity rankings          |
| `risk_combinations.csv`     | Multiple risk factor combinations       |
| `ga_ct_road_features.csv`   | State comparison of road features       |
| And 2 more... | |

**Key Results:**

|     Feature     | Severity Difference |       Effect         |
|-----------------|---------------------|----------------------|
| Traffic_Calming |        -0.423       | ✅ Reduces severity  |
| No_Exit         |        -0.373       | ✅ Reduces severity  |
| Traffic_Signal  |        -0.246       | ✅ Reduces severity  |
| Stop            |        +0.111       | ⚠️ Increases severity|

| Most Dangerous City | Severity |
|---------------------|----------|
| Pomfret Center, CT  |   3.02   |
| Kathleen, GA        |   2.98   |

|  Safest City  | Severity |
|---------------|----------|
| Hephzibah, GA | 1.98     |

---

### Step 6: Visualization (`visualization.py`)

**What it does:** Creates professional charts from all analysis results

**Input:** All CSV files from outputs/tables/

**Outputs (13 PNG files in `outputs/figures/`):**

| # |          Chart Name         |              File               |
|---|-----------------------------|---------------------------------|
| 1 | Severity Distribution (Bar) | `severity_distribution_bar.png` |
| 2 | Severity Distribution (Pie) | `severity_distribution_pie.png` |
| 3 | Time of Day Distribution    | `time_of_day_distribution.png`  |
| 4 | GA vs CT Comparison         | `ga_vs_ct_severity.png`         |  
| 5 | Top 10 Weather Conditions   | `top_10_weather_conditions.png` |
| 6 | Keyword Severity Impact     | `keyword_severity_impact.png`   |
| 7 | Road Features Impact        | `road_features_impact.png`      |
| 8 | Most Dangerous Cities       | `most_dangerous_cities.png`     |
| 9 | Risk Combinations           | `risk_combinations.png`         |
| 10 | Correlation Heatmap        | `correlation_heatmap.png`       |
| 11 | Weekend vs Weekday         | `weekend_vs_weekday.png`        |
| 12 | Day vs Night               | `day_vs_night.png`              |
| 13 | Wind Chill Severity        | `windchill_severity.png`        |

## How to Use This Code

### Prerequisites

| Requirement |       Details        |
|-------------|----------------------|
| Python      | 3.10 or higher       |
| Conda       | Anaconda or Miniconda|
| RAM         | 8GB minimum          |
| Storage     | 10GB free space      |

### Step 1: Setup Environment

```bash
# Create conda environment
conda create -n ds_project python=3.10 -y

# Activate environment
conda activate ds_project

# Install dependencies
pip install pandas numpy matplotlib seaborn scikit-learn scipy

Step 2: Download Dataset
Download the dataset from kaggle, link is on the top.

Step 3: Run the Project
bash
# Run all steps at once
python main.py

# OR run individual steps:
python filter.py              # Step 1: Filter GA & CT
python data_cleaning.py       # Step 2: Clean data
python statistical_analysis.py # Step 3: Statistics
python text_analysis.py       # Step 4: Text analysis
python advanced_features_analysis.py # Step 5: Road features
python visualization.py       # Step 6: Create charts

Step 4: View Outputs
Output	Location
Charts (13 PNG files)	outputs/figures/
Data tables (25+ CSV files)	outputs/tables/
Summary reports	outputs/reports/
File Descriptions
File	Purpose
filter.py	Filters 7.7M rows to GA & CT only
data_cleaning.py	Handles missing values, outliers, standardization
statistical_analysis.py	Calculates mean, median, correlation
text_analysis.py	Extracts keywords from descriptions
advanced_features_analysis.py	Analyzes road features, cities, counties
visualization.py	Creates all 13 charts
main.py	Runs all modules in sequence
Expected Output After Running
text
✅ filter.py: filtered_data.csv (240,239 rows)
✅ data_cleaning.py: cleaned_accidents.csv (240,225 rows)
✅ statistical_analysis.py: 11 CSV files created
✅ text_analysis.py: 7 CSV files created
✅ advanced_features_analysis.py: 7 CSV files created
✅ visualization.py: 13 PNG charts created

📁 Final Output Structure
text
outputs/
├── figures/                    # 13 PNG charts
│   ├── severity_distribution_bar.png
│   ├── severity_distribution_pie.png
│   └── ... (11 more)
│
├── tables/                     # 25+ CSV files
│   ├── numerical_statistics.csv
│   ├── severity_distribution.csv
│   ├── severity_correlations.csv
│   ├── specific_keyword_analysis.csv
│   ├── city_analysis.csv
│   ├── road_features_analysis.csv
│   └── ... (20+ more)
│
└── reports/                    # Summary text files
    ├── statistical_analysis_summary.txt
    └── text_analysis_summary.txt
Key                       Takeaways
Finding	                  Conclusion
Weather vs Severity	      ❌ No correlation (all < 0.07)
Text vs Severity	      ✅ Strong relationship ('jackknife' = 3.09)
Traffic Calming	          ✅ Most effective (-0.423 severity)
Morning Rush Hour	      ✅ Most accidents (34.8%)
Weekdays	              ✅ 5x more accidents than weekends
Roundabouts	              ✅ Junctions without = 63.9% severe

👤 Author
Name : Muhammad Ayyan
Student ID : 2403070032
Email : muhammad.ayyan@final.edu.tr
Course	AINE 312 - Data Science

📚 Citation
bibtex
@article{moosavi2019countrywide,
  title= A Countrywide Traffic Accident Dataset,
  author={Moosavi, Sobhan and Samavatian, Mohammad Hossein and Parthasarathy, Srinivasan and Ramnath, Rajiv},
  year={2019}
}
⭐ Star this repository if you found it useful!

#This README clearly explains:

1. **Step 1** - Filter.py (what it does, input, output)
2. **Step 2** - Data Cleaning (what it does, input, output)
3. **Step 3** - Statistical Analysis (outputs, key results)
4. **Step 4** - Text Analysis (outputs, key results)
5. **Step 5** - Advanced Features (outputs, key results)
6. **Step 6** - Visualization (13 charts)

