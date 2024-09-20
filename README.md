# QUAL-D

## Introduction

Qual-D offers an interactive data analysis experience, allowing users to upload various dataset formats and generate detailed reports. The app performs essential data quality checks, including handling missing values, detecting duplicates, and identifying outliers using advanced techniques like Z-score, IQR, and Mode Deviation. It also provides insights into the dataset's structure, such as unique values, data types, and timeliness checks for time-series data.
    <br><br>  Additionally, users can visualize correlations and summary statistics, making this app a powerful tool for data validation and exploratory analysis.

## Features Overview
### 1. File Upload:

Supports various file types: .csv, .xlsx, .xls, .json, .txt.<br>
Automatically handles file reading based on the selected file format.<br>
Displays the uploaded data in a dataframe.<br>

### 2.Data Quality Checks:

#### Missing Values and Duplicates:
Displays missing values, their count, and a summary of duplicates in the dataset.<br>
#### Null Columns:
Identifies and lists completely empty columns.<br>
#### Data Types:
Lists the data types of each column, grouped into numerical and categorical.<br>
#### Unique Values:
Allows selecting columns to see the unique values.<br>

### 3.Outlier Detection:

#### Categorical Columns:
Outlier detection via Frequency Analysis or Mode Deviation.<br>
#### Numerical Columns:
Detects outliers using Z-Score, IQR, and Flooring & Capping techniques.<br>
Visualizes outliers with a boxplot.

### 4.Timeliness Check:

Identifies gaps in time-series data and checks the last updated date.<br>
Ensures frequency consistency in date columns.
### 5.Descriptive Statistics:

Allows selection of numerical columns for descriptive analysis (mean, median, mode, standard deviation).
