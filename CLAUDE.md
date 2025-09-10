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

- `streamlit_app.py`: **Main Streamlit web application** for interactive data analysis with file upload
- `docs/пример1.py`: Original data analysis script that processes sales data from `sample_sales_data.xlsx`
- `docs/пример1.ipynb`: Original Jupyter notebook (generated from Google Colab)
- `docs/sample_sales_data.xlsx`: Sample Excel file containing monthly sales data for three products from 2020-2025
- `requirements.txt`: Complete list of Python dependencies
- `tests/`: Comprehensive test suite with unit, integration, and quality tests
- `pytest.ini`: Pytest configuration file
- `tests/conftest.py`: Shared test fixtures and configuration

## Development Environment

This project is developed in:
- **Python 3.13+**: Data analysis using pandas and matplotlib
- **Virtual Environment**: Use `python -m venv venv` and `.\venv\Scripts\activate` (Windows)
- **Jupyter Notebooks**: Interactive development environment (Google Colab origin)
- **Excel**: Data storage format (.xlsx files)

## Data Analysis Workflow

The main analysis script (`пример1.py`) performs:

1. **Data Loading**: Loads Excel data using pandas
2. **Data Overview**: Displays data types and basic information
3. **Statistical Analysis**: Calculates descriptive statistics for numerical columns
4. **Data Analysis**: Groups data, calculates totals and averages, identifies trends
5. **Visualization**: Creates time series plots and bar charts using matplotlib
6. **Reporting**: Generates detailed analysis report in both Russian and English

## Required Dependencies

Install from requirements file: `pip install -r requirements.txt`

Or install core packages manually: `pip install streamlit pandas openpyxl matplotlib seaborn`

Core libraries:
- `pandas`: Data manipulation and analysis
- `matplotlib`: Data visualization and plotting
- `openpyxl`: Excel file reading/writing
- `seaborn`: Statistical data visualization (optional enhancement)
- `streamlit`: Web app framework for interactive dashboards
- Standard datetime handling for time series analysis

## Development Commands

### Environment Setup
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
.\venv\Scripts\activate

# Install dependencies from requirements file
pip install -r requirements.txt

# Or install core packages manually
pip install streamlit pandas openpyxl matplotlib seaborn
```

### Running the Analysis
```bash
# Run the main analysis script (requires fixing file path)
python docs/пример1.py

# Start Streamlit web application
python -m streamlit run streamlit_app.py
# App will be available at: http://localhost:8501
```

### Testing Commands
```bash
# Install testing dependencies
pip install pytest pytest-cov

# Run all tests
python -m pytest tests/ -v

# Run specific test categories
python -m pytest tests/test_analysis_functions.py -v    # Unit tests
python -m pytest tests/test_streamlit_integration.py -v # Integration tests  
python -m pytest tests/test_code_quality.py -v         # Code quality tests
python -m pytest tests/test_data_samples.py -v         # Data samples tests

# Run tests with coverage report
python -m pytest tests/ --cov=streamlit_app --cov-report=term-missing

# Run only fast tests (skip slow performance tests)
python -m pytest tests/ -v -m "not slow"

# Run performance tests
python -m pytest tests/ -v -m "performance"

# Run comprehensive test suite
python tests/run_tests.py

# Run with performance tests included
python tests/run_tests.py --performance
```

## Streamlit Web Application Features

The main `streamlit_app.py` provides:
- **File Upload**: Drag-and-drop Excel file upload interface
- **Sample Data**: Built-in button to load example dataset
- **Interactive Analysis**: Real-time data processing and visualization
- **Multiple Visualizations**: Time series plots, bar charts, correlation heatmaps
- **Statistical Reports**: Comprehensive analysis with downloadable reports
- **Responsive Design**: Clean, professional web interface in Russian

## Working with This Codebase

When working with this project:
- **Main Interface**: Use Streamlit app (`streamlit_app.py`) for interactive analysis
- **Language**: Interface and analysis in Russian with bilingual documentation
- **Data Format**: Excel files (.xlsx) with automatic format detection
- **Visualizations**: matplotlib and seaborn with Russian labels
- **Code Structure**: Streamlit follows modern Python practices, original code follows Jupyter format
- **Time Series**: Data spans from 2020 to 2025
- **Products**: Analysis focuses on three products: Продукт_1, Продукт_2, Продукт_3
- **Virtual Environment**: Always activate venv before running applications

## Testing Architecture

The project includes comprehensive testing with:

### Test Categories:
- **Unit Tests** (`test_analysis_functions.py`): Test individual functions with various data scenarios
- **Integration Tests** (`test_streamlit_integration.py`): Test full application workflow and component integration  
- **Code Quality Tests** (`test_code_quality.py`): Syntax validation, code structure, security checks
- **Data Sample Tests** (`test_data_samples.py`): Tests with realistic data scenarios and edge cases

### Test Features:
- **Fixtures**: Shared test data and configurations in `conftest.py`
- **Performance Testing**: Marked with `@pytest.mark.slow` and `@pytest.mark.performance`
- **Mocking**: Streamlit components mocked for unit testing
- **Coverage Analysis**: Code coverage reporting with pytest-cov
- **Automated Test Runner**: `tests/run_tests.py` for comprehensive testing

### Running Tests:
- Use `python tests/run_tests.py` for full automated test suite
- Individual test files can be run separately with pytest
- Performance tests are optional and marked separately

## Known Issues

1. **File Path**: The script references `/content/drive/MyDrive/docs/sample_sales_data.xlsx` (Google Colab path) 
   - Update to: `docs/sample_sales_data.xlsx` for local development  
   - **Fixed in Streamlit app**: Automatically handles local paths
2. **Character Encoding**: Windows console may have issues displaying Cyrillic characters
3. **Virtual Environment**: Script may fail if dependencies not installed in activated venv

## File Naming Convention

Files use Cyrillic names (`пример1`) reflecting the Russian language context of the project.