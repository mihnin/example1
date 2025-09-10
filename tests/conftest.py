# -*- coding: utf-8 -*-
"""
Конфигурация pytest и общие фикстуры для тестов
"""

import pytest
import pandas as pd
import tempfile
import os
from datetime import datetime
import numpy as np


@pytest.fixture
def sample_sales_data():
    """Фикстура с образцовыми данными о продажах"""
    return pd.DataFrame({
        'Дата': pd.date_range('2020-01-01', periods=12, freq='MS'),
        'Продукт_1': [1000, 1100, 1200, 1150, 1300, 1250, 1400, 1350, 1450, 1500, 1550, 1600],
        'Продукт_2': [1500, 1400, 1600, 1550, 1700, 1650, 1800, 1750, 1850, 1900, 1950, 2000],
        'Продукт_3': [800, 850, 900, 875, 950, 925, 1000, 975, 1050, 1100, 1150, 1200]
    })


@pytest.fixture
def minimal_data():
    """Фикстура с минимальными данными"""
    return pd.DataFrame({
        'A': [10, 20],
        'B': [15, 25]
    })


@pytest.fixture
def data_with_nan():
    """Фикстура с данными, содержащими NaN значения"""
    return pd.DataFrame({
        'Дата': pd.date_range('2020-01-01', periods=5, freq='MS'),
        'Продукт_1': [100, np.nan, 300, 400, np.nan],
        'Продукт_2': [200, 250, np.nan, 350, 400],
        'Продукт_3': [50, 75, 100, np.nan, 150]
    })


@pytest.fixture
def large_dataset():
    """Фикстура с большим набором данных для тестов производительности"""
    np.random.seed(42)
    dates = pd.date_range('2000-01-01', periods=500, freq='MS')
    data = {
        'Дата': dates,
        'Продукт_1': np.random.randint(500, 2000, 500),
        'Продукт_2': np.random.randint(800, 2500, 500),
        'Продукт_3': np.random.randint(300, 1500, 500),
        'Продукт_4': np.random.randint(600, 1800, 500),
        'Продукт_5': np.random.randint(400, 1200, 500)
    }
    return pd.DataFrame(data)


@pytest.fixture
def temp_excel_file(sample_sales_data):
    """Фикстура создания временного Excel файла"""
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx')
    sample_sales_data.to_excel(temp_file.name, index=False)
    temp_file.close()
    
    yield temp_file.name
    
    # Очистка после теста
    if os.path.exists(temp_file.name):
        os.unlink(temp_file.name)


@pytest.fixture
def corrupted_data():
    """Фикстура с поврежденными данными"""
    return pd.DataFrame({
        'InvalidColumn': ['text', 'data', 'only'],
        'AnotherInvalid': ['more', 'text', 'here']
    })


@pytest.fixture
def mixed_data_types():
    """Фикстура со смешанными типами данных"""
    return pd.DataFrame({
        'Дата': pd.date_range('2020-01-01', periods=3, freq='MS'),
        'Numbers': [100, 200, 300],
        'Mixed': [100, 'text', 300],
        'Strings': ['A', 'B', 'C']
    })


@pytest.fixture(scope="session")
def test_output_dir():
    """Фикстура для создания директории вывода тестов"""
    output_dir = tempfile.mkdtemp(prefix="test_output_")
    yield output_dir
    
    # Очистка после всех тестов
    import shutil
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)


@pytest.fixture(autouse=True)
def setup_test_environment():
    """Автоматическая фикстура для настройки тестового окружения"""
    # Настройки перед каждым тестом
    import matplotlib
    matplotlib.use('Agg')  # Использовать backend без GUI для тестов
    
    # Подавление предупреждений pandas
    import warnings
    warnings.filterwarnings('ignore', category=pd.errors.PerformanceWarning)
    warnings.filterwarnings('ignore', category=FutureWarning)
    
    yield
    
    # Очистка после каждого теста
    import matplotlib.pyplot as plt
    plt.close('all')  # Закрыть все matplotlib фигуры


@pytest.fixture
def mock_streamlit():
    """Мок Streamlit для тестирования"""
    from unittest.mock import MagicMock
    
    mock_st = MagicMock()
    
    # Настройка основных методов Streamlit
    mock_st.title = MagicMock()
    mock_st.header = MagicMock()
    mock_st.subheader = MagicMock()
    mock_st.write = MagicMock()
    mock_st.dataframe = MagicMock()
    mock_st.pyplot = MagicMock()
    mock_st.metric = MagicMock()
    mock_st.columns = MagicMock(return_value=[MagicMock(), MagicMock(), MagicMock()])
    mock_st.session_state = {}
    
    # Настройка sidebar
    mock_st.sidebar = MagicMock()
    mock_st.sidebar.file_uploader = MagicMock(return_value=None)
    mock_st.sidebar.button = MagicMock(return_value=False)
    mock_st.sidebar.header = MagicMock()
    mock_st.sidebar.success = MagicMock()
    mock_st.sidebar.error = MagicMock()
    
    # Другие компоненты
    mock_st.info = MagicMock()
    mock_st.error = MagicMock()
    mock_st.success = MagicMock()
    mock_st.warning = MagicMock()
    mock_st.download_button = MagicMock()
    
    return mock_st


# Маркеры для категоризации тестов
pytest.mark.unit = pytest.mark.unit
pytest.mark.integration = pytest.mark.integration
pytest.mark.quality = pytest.mark.quality
pytest.mark.slow = pytest.mark.slow
pytest.mark.performance = pytest.mark.performance


def pytest_configure(config):
    """Конфигурация pytest при запуске"""
    # Добавляем кастомные маркеры
    config.addinivalue_line(
        "markers", "unit: Юнит-тесты отдельных функций"
    )
    config.addinivalue_line(
        "markers", "integration: Интеграционные тесты"
    )
    config.addinivalue_line(
        "markers", "quality: Тесты качества кода"
    )
    config.addinivalue_line(
        "markers", "slow: Медленные тесты (> 1 секунды)"
    )
    config.addinivalue_line(
        "markers", "performance: Тесты производительности"
    )


def pytest_collection_modifyitems(config, items):
    """Модификация собранных тестов"""
    # Автоматически помечаем тесты по названию файлов
    for item in items:
        # Помечаем тесты по файлам
        if "test_analysis_functions" in item.nodeid:
            item.add_marker(pytest.mark.unit)
        elif "test_streamlit_integration" in item.nodeid:
            item.add_marker(pytest.mark.integration)
        elif "test_code_quality" in item.nodeid:
            item.add_marker(pytest.mark.quality)
        
        # Помечаем медленные тесты
        if "performance" in item.name.lower() or "large" in item.name.lower():
            item.add_marker(pytest.mark.slow)
            item.add_marker(pytest.mark.performance)


def pytest_report_header(config):
    """Заголовок отчета pytest"""
    return [
        "Тестирование приложения анализа данных о продажах",
        f"Python версия: {os.sys.version}",
        f"Рабочая директория: {os.getcwd()}"
    ]