# GSOD Data Analysis - Task 1

## Dataset
This project uses a subset of the NOAA GSOD dataset:
- Years: 2020–2022
- Stations: 45 weather stations

The dataset is not included due to size.

## How to Run

### 1. Install dependencies
pip install -r requirements.txt

### 2. Download GSOD data (subset)
Download CSV files from:
https://noaa-gsod-pds.s3.amazonaws.com/index.html

Place them in:
data/2020/
data/2021/
data/2022/

### 3. Run preprocessing (Task 2)
python Task2/task2.py

(This generates the processed data required for the dashboard.)

### 4. Run dashboard (Task 4)
1. In terminal, paste: streamlit run task4_dashboard.py
2. Then open the local URL shown in the terminal (http://localhost:8501)

## Output

### Task 1:
- Schema inspection
- Record counts
- Station counts
- Missing value analysis
- Summary statistics

### Task 2:
- Data cleaning and preprocessing
- Outputs dataset used by dashboard

### Task 3:
- MapReduce implementation (mapper and reducer)

### Task 4 Dashboard:
- Interactive data exploration
- Visualizations of weather trends
- Filtering by year and station
