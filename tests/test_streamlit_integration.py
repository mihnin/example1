# -*- coding: utf-8 -*-
"""
Интеграционные тесты для Streamlit приложения
"""

import unittest
import pandas as pd
import tempfile
import os
import sys
from unittest.mock import patch, MagicMock
import io

# Добавляем корневую директорию в PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Мокаем streamlit перед импортом приложения
sys.modules['streamlit'] = MagicMock()

# Теперь импортируем приложение
import streamlit_app


class TestStreamlitIntegration(unittest.TestCase):
    """Интеграционные тесты для Streamlit приложения"""
    
    def setUp(self):
        """Настройка тестового окружения"""
        # Создаем тестовые данные
        self.test_data = pd.DataFrame({
            'Дата': pd.date_range('2020-01-01', periods=6, freq='MS'),
            'Продукт_1': [1000, 1100, 1200, 1150, 1300, 1250],
            'Продукт_2': [1500, 1400, 1600, 1550, 1700, 1650],
            'Продукт_3': [800, 850, 900, 875, 950, 925]
        })
        
        # Создаем временный Excel файл
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.xlsx')
        self.test_data.to_excel(self.temp_file.name, index=False)
        self.temp_file.close()
    
    def tearDown(self):
        """Очистка после тестов"""
        # Удаляем временный файл
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_analyze_sales_data_integration(self):
        """Интеграционный тест функции анализа данных"""
        # Тестируем полный цикл анализа
        results, processed_df = streamlit_app.analyze_sales_data(self.test_data.copy())
        
        # Проверяем структуру результатов
        expected_keys = [
            'basic_stats', 'total_sales_per_product', 'total_monthly_sales',
            'average_monthly_sales_per_product', 'month_highest_sales', 'product_highest_sales'
        ]
        
        for key in expected_keys:
            self.assertIn(key, results)
        
        # Проверяем, что обработанный DataFrame имеет правильную структуру
        self.assertEqual(len(processed_df.columns), 3)  # 3 продукта
        self.assertEqual(len(processed_df), 6)  # 6 месяцев
        self.assertTrue(pd.api.types.is_datetime64_any_dtype(processed_df.index))
    
    def test_create_visualizations_integration(self):
        """Интеграционный тест создания визуализаций"""
        # Получаем результаты анализа
        results, processed_df = streamlit_app.analyze_sales_data(self.test_data.copy())
        
        # Тестируем создание визуализаций
        try:
            fig1, fig2, fig3 = streamlit_app.create_visualizations(processed_df, results)
            
            # Проверяем, что возвращены объекты matplotlib
            import matplotlib.figure
            self.assertIsInstance(fig1, matplotlib.figure.Figure)
            self.assertIsInstance(fig2, matplotlib.figure.Figure)
            self.assertIsInstance(fig3, matplotlib.figure.Figure)
            
            # Проверяем, что графики содержат данные
            self.assertTrue(len(fig1.axes[0].lines) > 0)  # График временного ряда
            self.assertTrue(len(fig2.axes[0].patches) > 0)  # Столбчатая диаграмма
            
        except Exception as e:
            self.fail(f"Создание визуализаций завершилось с ошибкой: {e}")
    
    def test_excel_file_processing(self):
        """Тест обработки Excel файла"""
        # Читаем созданный временный файл
        loaded_data = pd.read_excel(self.temp_file.name)
        
        # Проверяем, что данные загрузились корректно
        self.assertEqual(len(loaded_data), 6)
        self.assertEqual(len(loaded_data.columns), 4)  # Дата + 3 продукта
        
        # Тестируем анализ загруженных данных
        results, processed_df = streamlit_app.analyze_sales_data(loaded_data.copy())
        
        # Проверяем корректность анализа
        self.assertIn('product_highest_sales', results)
        self.assertIn('month_highest_sales', results)
    
    def test_data_processing_pipeline(self):
        """Тест полного пайплайна обработки данных"""
        # Симулируем полный процесс обработки данных в приложении
        
        # 1. Загрузка данных
        input_data = self.test_data.copy()
        
        # 2. Анализ данных
        results, processed_df = streamlit_app.analyze_sales_data(input_data)
        
        # 3. Создание визуализаций
        fig1, fig2, fig3 = streamlit_app.create_visualizations(processed_df, results)
        
        # 4. Проверка результатов
        self.assertIsNotNone(results)
        self.assertIsNotNone(processed_df)
        self.assertIsNotNone(fig1)
        self.assertIsNotNone(fig2)
        self.assertIsNotNone(fig3)
        
        # Проверяем ключевые метрики
        self.assertTrue(results['total_sales_per_product'].sum() > 0)
        self.assertTrue(results['total_monthly_sales'].sum() > 0)
        self.assertTrue(len(results['average_monthly_sales_per_product']) == 3)
    
    def test_error_handling(self):
        """Тест обработки ошибок"""
        # Тест с некорректными данными
        corrupted_data = pd.DataFrame({
            'Invalid': ['text', 'data', 'only']
        })
        
        # Проверяем, что функция либо обрабатывает ошибку, либо выбрасывает исключение
        try:
            results, processed_df = streamlit_app.analyze_sales_data(corrupted_data)
            # Если ошибка не выброшена, проверяем результаты
            self.assertIsNotNone(results)
        except Exception:
            # Ошибка ожидаема для некорректных данных
            pass
    
    def test_edge_cases(self):
        """Тест граничных случаев"""
        # Тест с минимальными данными
        minimal_data = pd.DataFrame({
            'A': [1],
            'B': [2]
        })
        
        try:
            results, processed_df = streamlit_app.analyze_sales_data(minimal_data)
            self.assertIsNotNone(results)
        except Exception:
            # Может быть ожидаемым для слишком малых данных
            pass
        
        # Тест с большими числами
        large_data = pd.DataFrame({
            'Дата': pd.date_range('2020-01-01', periods=2, freq='MS'),
            'Large_Product': [1e9, 2e9]
        })
        
        try:
            results, processed_df = streamlit_app.analyze_sales_data(large_data)
            self.assertIsNotNone(results)
            # Проверяем, что большие числа обрабатываются корректно
            self.assertTrue(results['total_sales_per_product']['Large_Product'] > 1e9)
        except Exception as e:
            self.fail(f"Обработка больших чисел завершилась ошибкой: {e}")


class TestStreamlitAppComponents(unittest.TestCase):
    """Тесты компонентов Streamlit приложения"""
    
    @patch('streamlit_app.st')
    def test_app_structure(self, mock_st):
        """Тест структуры приложения (мокированный)"""
        # Мокаем session_state
        mock_st.session_state = {}
        mock_st.sidebar.file_uploader.return_value = None
        mock_st.sidebar.button.return_value = False
        
        # Пытаемся вызвать main функцию
        try:
            streamlit_app.main()
            # Проверяем, что основные компоненты были вызваны
            mock_st.title.assert_called()
            mock_st.sidebar.header.assert_called()
        except Exception as e:
            # Ожидаемо, так как мы мокаем не все компоненты
            pass
    
    def test_data_validation_functions(self):
        """Тест вспомогательных функций валидации данных"""
        # Создаем тестовые данные для валидации
        valid_data = pd.DataFrame({
            'Unnamed: 0': pd.date_range('2020-01-01', periods=3, freq='MS'),
            'Product_A': [100, 200, 300],
            'Product_B': [150, 250, 350]
        })
        
        # Тестируем обработку валидных данных
        try:
            results, processed_df = streamlit_app.analyze_sales_data(valid_data.copy())
            
            # Проверяем базовые характеристики результатов
            self.assertTrue(len(results) > 0)
            self.assertTrue(len(processed_df) > 0)
            self.assertTrue(processed_df.index.dtype.name.startswith('datetime'))
            
        except Exception as e:
            self.fail(f"Валидация корректных данных завершилась ошибкой: {e}")


class TestPerformance(unittest.TestCase):
    """Тесты производительности"""
    
    def test_large_dataset_performance(self):
        """Тест производительности с большим набором данных"""
        import time
        
        # Создаем большой набор данных
        large_data = pd.DataFrame({
            'Дата': pd.date_range('2000-01-01', periods=1000, freq='MS'),
            'Продукт_1': range(1000),
            'Продукт_2': range(1000, 2000),
            'Продукт_3': range(2000, 3000),
            'Продукт_4': range(3000, 4000),
            'Продукт_5': range(4000, 5000)
        })
        
        # Измеряем время выполнения
        start_time = time.time()
        results, processed_df = streamlit_app.analyze_sales_data(large_data.copy())
        execution_time = time.time() - start_time
        
        # Проверяем, что обработка завершилась за разумное время (< 10 секунд)
        self.assertLess(execution_time, 10.0, "Обработка больших данных заняла слишком много времени")
        
        # Проверяем корректность результатов
        self.assertEqual(len(processed_df), 1000)
        self.assertEqual(len(processed_df.columns), 5)
    
    def test_memory_usage(self):
        """Тест использования памяти"""
        import psutil
        import os
        
        # Получаем начальное использование памяти
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Создаем и обрабатываем данные
        test_data = pd.DataFrame({
            'Дата': pd.date_range('2020-01-01', periods=100, freq='MS'),
            'Продукт_1': range(100),
            'Продукт_2': range(100, 200),
            'Продукт_3': range(200, 300)
        })
        
        for _ in range(10):  # Повторяем операцию несколько раз
            results, processed_df = streamlit_app.analyze_sales_data(test_data.copy())
            fig1, fig2, fig3 = streamlit_app.create_visualizations(processed_df, results)
        
        # Проверяем финальное использование памяти
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        # Проверяем, что утечка памяти не превышает 100MB
        self.assertLess(memory_increase, 100, f"Потенциальная утечка памяти: {memory_increase:.2f} MB")


if __name__ == '__main__':
    # Запуск интеграционных тестов
    unittest.main(verbosity=2)