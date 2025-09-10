# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a data analysis example project (`example1`) containing sales data analysis code. The project demonstrates:

- Data analysis workflow using pandas and matplotlib
- Processing Excel files with sales data
- Statistical analysis and visualization of time series sales data
- Bilingual documentation (Russian/English)

## Repository Structure

```
C:\dev\example1\
├── docs/                    # Documentation and data files
│   ├── sample_sales_data.xlsx   # Sample Excel data file
│   ├── пример1.ipynb           # Jupyter notebook (Russian)
│   └── пример1.py              # Python script converted from notebook
├── README.md               # Basic project description
└── LICENSE                # Project license
```

## Key Files

- `docs/пример1.py`: Main data analysis script that processes sales data from `sample_sales_data.xlsx`
- `docs/пример1.ipynb`: Original Jupyter notebook (generated from Google Colab)
- `docs/sample_sales_data.xlsx`: Sample Excel file containing monthly sales data for three products from 2020-2025

## Development Environment

This project appears to be developed primarily in:
- **Python**: Data analysis using pandas and matplotlib
- **Jupyter Notebooks**: Interactive development environment
- **Excel**: Data storage format

## Data Analysis Workflow

The main analysis script (`пример1.py`) performs:

1. **Data Loading**: Loads Excel data using pandas
2. **Data Overview**: Displays data types and basic information
3. **Statistical Analysis**: Calculates descriptive statistics for numerical columns
4. **Data Analysis**: Groups data, calculates totals and averages, identifies trends
5. **Visualization**: Creates time series plots and bar charts using matplotlib
6. **Reporting**: Generates detailed analysis report in both Russian and English

## Key Libraries Used

- `pandas`: Data manipulation and analysis
- `matplotlib.pyplot`: Data visualization
- Standard datetime handling for time series analysis

## Working with This Codebase

When working with this project:
- The main analysis code is in Russian with English summaries
- Data files are Excel format (.xlsx)
- Visualizations use matplotlib with Russian labels
- Code follows Jupyter notebook structure (converted to .py format)
- Time series data spans from 2020 to 2025
- Analysis focuses on three products: Продукт_1, Продукт_2, Продукт_3

## File Naming Convention

Files use Cyrillic names (`пример1`) reflecting the Russian language context of the project.