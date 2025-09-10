# -*- coding: utf-8 -*-
"""
Юнит-тесты для функций анализа данных
"""

import unittest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# Добавляем корневую директорию в PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from streamlit_app import analyze_sales_data, create_visualizations


class TestAnalysisFunctions(unittest.TestCase):
    """Тестовый класс для функций анализа данных"""
    
    def setUp(self):
        """Настройка тестовых данных перед каждым тестом"""
        # Создаем тестовый DataFrame
        dates = pd.date_range('2020-01-01', periods=12, freq='MS')
        self.test_df = pd.DataFrame({
            'Unnamed: 0': dates,
            'Продукт_1': [1000, 1100, 1200, 1150, 1300, 1250, 1400, 1350, 1450, 1500, 1550, 1600],
            'Продукт_2': [1500, 1400, 1600, 1550, 1700, 1650, 1800, 1750, 1850, 1900, 1950, 2000],
            'Продукт_3': [800, 850, 900, 875, 950, 925, 1000, 975, 1050, 1100, 1150, 1200]
        })
        
        # Создаем простой DataFrame без дат
        self.simple_df = pd.DataFrame({
            'A': [10, 20, 30],
            'B': [15, 25, 35],
            'C': [5, 10, 15]
        })
        
        # Создаем DataFrame с пропущенными значениями
        self.df_with_nan = pd.DataFrame({
            'Unnamed: 0': pd.date_range('2020-01-01', periods=3, freq='MS'),
            'Продукт_1': [100, np.nan, 300],
            'Продукт_2': [200, 250, np.nan],
            'Продукт_3': [50, 75, 100]
        })
    
    def test_analyze_sales_data_basic(self):
        """Тест базового функционала analyze_sales_data"""
        results, processed_df = analyze_sales_data(self.test_df.copy())
        
        # Проверяем, что все ключи присутствуют в результатах
        expected_keys = [
            'basic_stats', 'total_sales_per_product', 'total_monthly_sales',
            'average_monthly_sales_per_product', 'month_highest_sales', 'product_highest_sales'
        ]
        
        for key in expected_keys:
            self.assertIn(key, results, f"Ключ '{key}' отсутствует в результатах")
        
        # Проверяем типы данных
        self.assertIsInstance(results['basic_stats'], pd.DataFrame)
        self.assertIsInstance(results['total_sales_per_product'], pd.Series)
        self.assertIsInstance(results['total_monthly_sales'], pd.Series)
        self.assertIsInstance(results['average_monthly_sales_per_product'], pd.Series)
        
        # Проверяем, что индекс обработанного DataFrame содержит даты
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(processed_df.index))
    
    def test_analyze_sales_data_calculations(self):
        """Тест правильности вычислений в analyze_sales_data"""
        results, processed_df = analyze_sales_data(self.test_df.copy())
        
        # Проверяем общие продажи по продуктам
        expected_total_product1 = sum(self.test_df['Продукт_1'])
        self.assertEqual(results['total_sales_per_product']['Продукт_1'], expected_total_product1)
        
        # Проверяем средние значения
        expected_avg_product1 = self.test_df['Продукт_1'].mean()
        self.assertAlmostEqual(
            results['average_monthly_sales_per_product']['Продукт_1'], 
            expected_avg_product1, 
            places=2
        )
        
        # Проверяем общие ежемесячные продажи
        first_month_total = self.test_df.iloc[0, 1:].sum()  # Сумма первого месяца
        self.assertEqual(results['total_monthly_sales'].iloc[0], first_month_total)
        
        # Проверяем продукт с наивысшими продажами
        max_product = results['total_sales_per_product'].idxmax()
        self.assertEqual(results['product_highest_sales'], max_product)
    
    def test_analyze_sales_data_with_simple_dataframe(self):
        """Тест с простым DataFrame без столбца дат"""
        results, processed_df = analyze_sales_data(self.simple_df.copy())
        
        # Проверяем, что анализ работает даже без дат
        self.assertIn('basic_stats', results)
        self.assertIn('total_sales_per_product', results)
        
        # Проверяем размеры результатов
        self.assertEqual(len(results['total_sales_per_product']), 3)
        self.assertEqual(len(results['average_monthly_sales_per_product']), 3)
    
    def test_analyze_sales_data_with_nan_values(self):
        """Тест обработки пропущенных значений"""
        results, processed_df = analyze_sales_data(self.df_with_nan.copy())
        
        # Проверяем, что функция работает с NaN значениями
        self.assertIn('basic_stats', results)
        
        # Проверяем, что NaN значения корректно обработаны в статистике
        stats = results['basic_stats']
        self.assertTrue(stats.loc['count', 'Продукт_1'] == 2)  # Должно быть 2 валидных значения
        self.assertTrue(stats.loc['count', 'Продукт_2'] == 2)  # Должно быть 2 валидных значения
    
    def test_analyze_sales_data_empty_dataframe(self):
        """Тест с пустым DataFrame"""
        empty_df = pd.DataFrame()
        
        with self.assertRaises(Exception):
            analyze_sales_data(empty_df)
    
    def test_analyze_sales_data_single_row(self):
        """Тест с DataFrame из одной строки"""
        single_row_df = pd.DataFrame({
            'A': [100],
            'B': [200],
            'C': [300]
        })
        
        results, processed_df = analyze_sales_data(single_row_df.copy())
        
        # Проверяем, что результаты получены
        self.assertIn('total_sales_per_product', results)
        self.assertEqual(results['total_sales_per_product']['A'], 100)
        self.assertEqual(results['total_sales_per_product']['B'], 200)
        self.assertEqual(results['total_sales_per_product']['C'], 300)
    
    def test_create_visualizations_basic(self):
        """Тест создания визуализаций"""
        results, processed_df = analyze_sales_data(self.test_df.copy())
        
        try:
            fig1, fig2, fig3 = create_visualizations(processed_df, results)
            
            # Проверяем, что возвращены matplotlib фигуры
            import matplotlib.figure
            self.assertIsInstance(fig1, matplotlib.figure.Figure)
            self.assertIsInstance(fig2, matplotlib.figure.Figure)
            self.assertIsInstance(fig3, matplotlib.figure.Figure)
            
            # Проверяем, что фигуры имеют оси
            self.assertTrue(len(fig1.axes) > 0)
            self.assertTrue(len(fig2.axes) > 0)
            self.assertTrue(len(fig3.axes) > 0)
            
        except Exception as e:
            self.fail(f"create_visualizations выбросила исключение: {e}")
    
    def test_data_types_consistency(self):
        """Тест консистентности типов данных"""
        results, processed_df = analyze_sales_data(self.test_df.copy())
        
        # Проверяем, что числовые результаты действительно числовые
        for value in results['total_sales_per_product']:
            self.assertTrue(pd.api.types.is_numeric_dtype(type(value)))
        
        for value in results['average_monthly_sales_per_product']:
            self.assertTrue(pd.api.types.is_numeric_dtype(type(value)))
        
        for value in results['total_monthly_sales']:
            self.assertTrue(pd.api.types.is_numeric_dtype(type(value)))
    
    def test_index_preservation(self):
        """Тест сохранения индексов после обработки"""
        results, processed_df = analyze_sales_data(self.test_df.copy())
        
        # Проверяем, что количество строк не изменилось
        original_rows = len(self.test_df)
        processed_rows = len(processed_df)
        self.assertEqual(original_rows, processed_rows)
        
        # Проверяем, что колонки данных сохранились (минус колонка дат)
        expected_columns = len(self.test_df.columns) - 1  # -1 для колонки дат
        actual_columns = len(processed_df.columns)
        self.assertEqual(expected_columns, actual_columns)
    
    def test_statistical_calculations(self):
        """Тест статистических вычислений"""
        results, processed_df = analyze_sales_data(self.test_df.copy())
        
        # Проверяем основные статистические показатели
        stats = results['basic_stats']
        
        # Проверяем, что все ожидаемые статистики присутствуют
        expected_stats = ['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']
        for stat in expected_stats:
            self.assertIn(stat, stats.index)
        
        # Проверяем, что среднее значение меньше максимального
        for column in processed_df.columns:
            self.assertLess(stats.loc['mean', column], stats.loc['max', column])
            self.assertGreater(stats.loc['mean', column], stats.loc['min', column])


class TestDataValidation(unittest.TestCase):
    """Тесты валидации данных"""
    
    def test_invalid_data_types(self):
        """Тест с некорректными типами данных"""
        invalid_df = pd.DataFrame({
            'A': ['text', 'more text', 'even more text'],
            'B': [1, 2, 3]
        })
        
        # Функция должна работать, но результаты могут быть ограниченными
        try:
            results, processed_df = analyze_sales_data(invalid_df.copy())
            # Проверяем, что получили какие-то результаты
            self.assertIn('basic_stats', results)
        except Exception:
            # Допустимо, если функция выбрасывает исключение для некорректных данных
            pass
    
    def test_mixed_data_types(self):
        """Тест со смешанными типами данных"""
        mixed_df = pd.DataFrame({
            'Unnamed: 0': pd.date_range('2020-01-01', periods=3, freq='MS'),
            'Numbers': [100, 200, 300],
            'Mixed': [100, 'text', 300]
        })
        
        try:
            results, processed_df = analyze_sales_data(mixed_df.copy())
            # Проверяем, что обработка прошла
            self.assertIsNotNone(results)
        except Exception as e:
            # Логируем ошибку для отладки
            print(f"Expected exception with mixed data types: {e}")


if __name__ == '__main__':
    # Запуск тестов с подробным выводом
    unittest.main(verbosity=2)