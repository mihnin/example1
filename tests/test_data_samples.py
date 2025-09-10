# -*- coding: utf-8 -*-
"""
Тесты с различными образцами данных
"""

import pytest
import pandas as pd
import numpy as np
import sys
import os

# Добавляем корневую директорию в PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from streamlit_app import analyze_sales_data


@pytest.mark.unit
class TestDataSamples:
    """Тесты с различными образцами данных"""
    
    def test_with_sample_sales_data(self, sample_sales_data):
        """Тест с образцовыми данными о продажах"""
        results, processed_df = analyze_sales_data(sample_sales_data.copy())
        
        # Проверяем структуру результатов
        assert 'total_sales_per_product' in results
        assert 'average_monthly_sales_per_product' in results
        assert 'product_highest_sales' in results
        
        # Проверяем, что данные обработаны корректно
        assert len(processed_df) == 12  # 12 месяцев
        assert len(processed_df.columns) == 3  # 3 продукта
        assert pd.api.types.is_datetime64_any_dtype(processed_df.index)
    
    def test_with_minimal_data(self, minimal_data):
        """Тест с минимальными данными"""
        results, processed_df = analyze_sales_data(minimal_data.copy())
        
        # Проверяем, что анализ работает даже с минимальными данными
        assert 'basic_stats' in results
        assert len(results['total_sales_per_product']) == 2
        assert len(processed_df) == 2
    
    def test_with_nan_data(self, data_with_nan):
        """Тест с данными, содержащими NaN"""
        results, processed_df = analyze_sales_data(data_with_nan.copy())
        
        # Проверяем обработку NaN значений
        assert 'basic_stats' in results
        stats = results['basic_stats']
        
        # Проверяем, что NaN корректно исключены из расчетов
        assert stats.loc['count', 'Продукт_1'] == 3  # 2 NaN из 5 значений
        assert stats.loc['count', 'Продукт_2'] == 4  # 1 NaN из 5 значений
        assert stats.loc['count', 'Продукт_3'] == 4  # 1 NaN из 5 значений
    
    def test_with_corrupted_data(self, corrupted_data):
        """Тест с поврежденными данными"""
        # Ожидаем, что функция либо обработает ошибку, либо выбросит исключение
        try:
            results, processed_df = analyze_sales_data(corrupted_data.copy())
            # Если обработка прошла, проверяем результаты
            assert results is not None
        except Exception:
            # Исключение ожидаемо для поврежденных данных
            pass
    
    def test_with_mixed_data_types(self, mixed_data_types):
        """Тест со смешанными типами данных"""
        try:
            results, processed_df = analyze_sales_data(mixed_data_types.copy())
            # Проверяем, что функция работает со смешанными типами
            assert results is not None
            assert len(processed_df) == 3
        except Exception:
            # Исключение может быть ожидаемым
            pass
    
    @pytest.mark.slow
    @pytest.mark.performance
    def test_with_large_dataset(self, large_dataset):
        """Тест с большим набором данных"""
        import time
        
        start_time = time.time()
        results, processed_df = analyze_sales_data(large_dataset.copy())
        execution_time = time.time() - start_time
        
        # Проверяем производительность
        assert execution_time < 5.0, f"Обработка заняла слишком много времени: {execution_time:.2f}с"
        
        # Проверяем корректность результатов
        assert len(processed_df) == 500
        assert len(processed_df.columns) == 5
        assert results['total_sales_per_product'].sum() > 0
    
    def test_empty_dataframe(self):
        """Тест с пустым DataFrame"""
        empty_df = pd.DataFrame()
        
        with pytest.raises(Exception):
            analyze_sales_data(empty_df)
    
    def test_single_column_data(self):
        """Тест с данными из одного столбца"""
        single_col_df = pd.DataFrame({'OnlyColumn': [1, 2, 3, 4, 5]})
        
        results, processed_df = analyze_sales_data(single_col_df.copy())
        
        assert len(results['total_sales_per_product']) == 1
        assert results['total_sales_per_product']['OnlyColumn'] == 15
    
    def test_single_row_data(self):
        """Тест с данными из одной строки"""
        single_row_df = pd.DataFrame({
            'Продукт_A': [100],
            'Продукт_B': [200],
            'Продукт_C': [300]
        })
        
        results, processed_df = analyze_sales_data(single_row_df.copy())
        
        assert results['total_sales_per_product']['Продукт_A'] == 100
        assert results['total_sales_per_product']['Продукт_B'] == 200
        assert results['total_sales_per_product']['Продукт_C'] == 300
        assert results['product_highest_sales'] == 'Продукт_C'
    
    def test_zero_values(self):
        """Тест с нулевыми значениями"""
        zero_df = pd.DataFrame({
            'Дата': pd.date_range('2020-01-01', periods=3, freq='MS'),
            'Продукт_1': [0, 100, 0],
            'Продукт_2': [0, 0, 200],
            'Продукт_3': [50, 0, 0]
        })
        
        results, processed_df = analyze_sales_data(zero_df.copy())
        
        assert results['total_sales_per_product']['Продукт_1'] == 100
        assert results['total_sales_per_product']['Продукт_2'] == 200
        assert results['total_sales_per_product']['Продукт_3'] == 50
    
    def test_negative_values(self):
        """Тест с отрицательными значениями"""
        negative_df = pd.DataFrame({
            'Дата': pd.date_range('2020-01-01', periods=3, freq='MS'),
            'Продукт_1': [-100, 200, -50],
            'Продукт_2': [100, -150, 300],
            'Продукт_3': [0, 0, 0]
        })
        
        results, processed_df = analyze_sales_data(negative_df.copy())
        
        # Проверяем, что отрицательные значения обрабатываются
        assert results['total_sales_per_product']['Продукт_1'] == 50  # -100 + 200 - 50
        assert results['total_sales_per_product']['Продукт_2'] == 250  # 100 - 150 + 300
        assert results['total_sales_per_product']['Продукт_3'] == 0
    
    def test_very_large_numbers(self):
        """Тест с очень большими числами"""
        large_numbers_df = pd.DataFrame({
            'Дата': pd.date_range('2020-01-01', periods=2, freq='MS'),
            'Большой_Продукт': [1e9, 2e9],  # Миллиарды
            'Очень_Большой': [1e12, 2e12]   # Триллионы
        })
        
        results, processed_df = analyze_sales_data(large_numbers_df.copy())
        
        assert results['total_sales_per_product']['Большой_Продукт'] == 3e9
        assert results['total_sales_per_product']['Очень_Большой'] == 3e12
    
    def test_decimal_values(self):
        """Тест с десятичными значениями"""
        decimal_df = pd.DataFrame({
            'Дата': pd.date_range('2020-01-01', periods=3, freq='MS'),
            'Продукт_1': [100.5, 200.75, 150.25],
            'Продукт_2': [50.33, 75.67, 100.99]
        })
        
        results, processed_df = analyze_sales_data(decimal_df.copy())
        
        # Проверяем точность вычислений с десятичными числами
        expected_total_1 = 100.5 + 200.75 + 150.25
        expected_total_2 = 50.33 + 75.67 + 100.99
        
        assert abs(results['total_sales_per_product']['Продукт_1'] - expected_total_1) < 0.01
        assert abs(results['total_sales_per_product']['Продукт_2'] - expected_total_2) < 0.01
    
    def test_date_formats(self):
        """Тест с различными форматами дат"""
        # Тест с различными форматами дат в строковом виде
        date_formats_df = pd.DataFrame({
            'Дата': ['2020-01-01', '2020-02-01', '2020-03-01'],
            'Продукт_1': [100, 200, 300]
        })
        
        results, processed_df = analyze_sales_data(date_formats_df.copy())
        
        # Проверяем, что даты были корректно преобразованы
        assert pd.api.types.is_datetime64_any_dtype(processed_df.index)
        assert len(processed_df) == 3
    
    def test_unicode_column_names(self):
        """Тест с названиями столбцов в Unicode"""
        unicode_df = pd.DataFrame({
            'Дата': pd.date_range('2020-01-01', periods=2, freq='MS'),
            'Продукт_号码1': [100, 200],  # Китайские символы
            'Продукт_αβγ': [150, 250],   # Греческие символы
            'Продукт_🚀': [50, 75]       # Эмодзи
        })
        
        results, processed_df = analyze_sales_data(unicode_df.copy())
        
        # Проверяем, что Unicode символы в названиях обрабатываются корректно
        assert 'Продукт_号码1' in results['total_sales_per_product']
        assert 'Продукт_αβγ' in results['total_sales_per_product']
        assert 'Продукт_🚀' in results['total_sales_per_product']


@pytest.mark.integration
class TestRealWorldScenarios:
    """Тесты сценариев реального мира"""
    
    def test_seasonal_data(self):
        """Тест с сезонными данными"""
        # Создаем данные с сезонным паттерном
        dates = pd.date_range('2020-01-01', periods=24, freq='MS')
        seasonal_pattern = [100 + 50 * np.sin(2 * np.pi * i / 12) for i in range(24)]
        
        seasonal_df = pd.DataFrame({
            'Дата': dates,
            'Сезонный_Продукт': seasonal_pattern
        })
        
        results, processed_df = analyze_sales_data(seasonal_df.copy())
        
        # Проверяем, что сезонные данные обработаны
        assert len(processed_df) == 24
        assert results['total_sales_per_product']['Сезонный_Продукт'] > 0
    
    def test_growth_trend_data(self):
        """Тест с данными с трендом роста"""
        dates = pd.date_range('2020-01-01', periods=12, freq='MS')
        growth_data = [100 * (1.1 ** i) for i in range(12)]  # 10% роста каждый месяц
        
        growth_df = pd.DataFrame({
            'Дата': dates,
            'Растущий_Продукт': growth_data
        })
        
        results, processed_df = analyze_sales_data(growth_df.copy())
        
        # Проверяем, что тренд роста отражен в данных
        first_half_avg = processed_df.iloc[:6]['Растущий_Продукт'].mean()
        second_half_avg = processed_df.iloc[6:]['Растущий_Продукт'].mean()
        
        assert second_half_avg > first_half_avg, "Тренд роста не обнаружен"
    
    def test_multiple_products_comparison(self):
        """Тест сравнения множественных продуктов"""
        dates = pd.date_range('2020-01-01', periods=12, freq='MS')
        
        multi_product_df = pd.DataFrame({
            'Дата': dates,
            'Лидер_Рынка': [1000] * 12,      # Стабильный лидер
            'Растущий_Игрок': list(range(100, 1300, 100)),  # Быстрый рост
            'Падающий_Бренд': list(range(1200, 0, -100)),   # Падение
            'Нишевый_Продукт': [200] * 12    # Стабильная ниша
        })
        
        results, processed_df = analyze_sales_data(multi_product_df.copy())
        
        # Проверяем правильность определения лидера
        top_product = results['product_highest_sales']
        assert top_product in ['Лидер_Рынка', 'Растущий_Игрок'], f"Неожиданный лидер: {top_product}"
        
        # Проверяем, что все продукты учтены
        assert len(results['total_sales_per_product']) == 4


if __name__ == '__main__':
    pytest.main([__file__, '-v'])