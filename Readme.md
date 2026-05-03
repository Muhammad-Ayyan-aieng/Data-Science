# 🚗 US Accidents Analysis: Georgia vs Connecticut

**Course:** AINE 312 - Data Science | **Term:** Spring 2025/26 | **States:** GA & CT

---

## 📊 Project Overview

This project analyzes traffic accident data from Georgia (GA) and Connecticut (CT) using the US Accidents dataset (2016-2023). The analysis includes data filtering, cleaning, statistical analysis, text mining, and visualization.

---

## 📁 Dataset Source

**Original Dataset:** [US Accidents (2016 - 2023)](https://www.kaggle.com/datasets/sobhanmoosavi/us-accidents) by Sobhan Moosavi

|    Property    |    Value    |
|---------======-|-------------|
| Total Records  | 7,728,394   |
| Time Period    | 2016 - 2023 |
| File Size      | 3.06 GB     |
| License        | CC BY-NC-SA 4.0|

> ⚠️ For non-commercial research purposes only. Must cite original papers.

---

## 🔧 Project Structure
US-Accidents-Analysis/
│
├── datasets/
│ ├── US_Accidents_March23.csv # Original data
│ ├── filtered_data.csv # GA & CT only
│ └── cleaned_accidents.csv # Cleaned data
│
├── outputs/
│ ├── statistical_analysis/ # Stats results
│ ├── text_analysis/ # NLP results
│ ├── advanced_features/ # Road/geography results
│ ├── comparison_analysis/ # GA vs CT results
│ └── figures/ # Charts
│
├── filter.py # Step 1: Filter GA & CT
├── data_cleaning.py # Step 2: Clean data
├── statistical_analysis.py # Step 3: Statistics
├── text_analysis.py # Step 4: NLP on descriptions
├── advanced_features_analysis.py # Step 5: Road features
├── comparison_analysis.py # Step 6: GA vs CT
├── visualization.py # Step 7: Create charts
├── main.py # Run all modules
└── requirements.txt # Dependencies

text

---

## 🚀 How to Run

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
pip install -r requirements.txt
Step 2: Download Dataset
Download US_Accidents_March23.csv from Kaggle and place it in the datasets/ folder.

Step 3: Run the Project
bash
# Run all steps at once
python main.py

# OR run individual steps:
python filter.py                    # Step 1
python data_cleaning.py             # Step 2
python statistical_analysis.py      # Step 3
python text_analysis.py             # Step 4
python advanced_features_analysis.py # Step 5
python comparison_analysis.py       # Step 6
python visualization.py             # Step 7
📁 Processing Pipeline
Step	File	Description	Output
1	filter.py	Filters 7.7M rows to GA & CT only	filtered_data.csv
2	data_cleaning.py	Handles missing values, outliers, creates features	cleaned_accidents.csv
3	statistical_analysis.py	Calculates mean, median, correlations, distributions	CSV + Excel + Word
4	text_analysis.py	Extracts keywords from accident descriptions	CSV + Excel + Word
5	advanced_features_analysis.py	Analyzes road features, cities, counties, seasons	CSV + Excel + Word
6	comparison_analysis.py	Compares GA vs CT across multiple factors	CSV + Excel + Word
7	visualization.py	Creates professional charts	PNG files
📁 Output Structure
text
outputs/
├── statistical_analysis/
│   ├── tables/                     # CSV files
│   └── reports/                    # Excel + Word
│
├── text_analysis/
│   ├── tables/                     # CSV files
│   └── reports/                    # Excel + Word
│
├── advanced_features/
│   ├── tables/                     # CSV files
│   └── reports/                    # Excel + Word
│
├── comparison_analysis/
│   ├── tables/                     # CSV files
│   └── reports/                    # Excel + Word
│
└── figures/                        # PNG charts
🛠️ Tools Used
Tool	Version	Purpose
Python	3.10	Programming language
Pandas	2.0+	Data manipulation
NumPy	1.24+	Numerical operations
Scikit-learn	1.3+	Text vectorization
SciPy	1.10+	Statistical tests
Matplotlib	3.7+	Chart creation
Seaborn	0.12+	Enhanced visualizations
OpenPyXL	3.1+	Excel export
python-docx	1.0+	Word export
📚 Citation
If you use this dataset, please cite:

bibtex
@article{moosavi2019countrywide,
  title={A Countrywide Traffic Accident Dataset},
  author={Moosavi, Sobhan and Samavatian, Mohammad Hossein and 
          Parthasarathy, Srinivasan and Ramnath, Rajiv},
  year={2019}
}
👤 Author
Name	Muhammad Ayyan
Student ID	2403070032
Email	muhammad.ayyan@final.edu.tr
Course	AINE 312 - Data Science
Term	Spring 2025/26
📄 License
This project is for educational purposes only. The original dataset is licensed under CC BY-NC-SA 4.0.

⭐ Star this repository if you found it useful!

