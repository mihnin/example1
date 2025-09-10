# -*- coding: utf-8 -*-
"""
Тесты качества кода, синтаксиса и стиля
"""

import unittest
import ast
import os
import sys
import importlib.util
import py_compile
import tempfile
from pathlib import Path


class TestCodeSyntax(unittest.TestCase):
    """Тесты синтаксиса Python кода"""
    
    def setUp(self):
        """Настройка путей к файлам проекта"""
        self.project_root = Path(__file__).parent.parent
        self.python_files = [
            self.project_root / 'streamlit_app.py',
            self.project_root / 'docs' / 'пример1.py'
        ]
        
        # Добавляем все Python файлы из tests
        test_files = list((self.project_root / 'tests').glob('*.py'))
        self.python_files.extend(test_files)
    
    def test_python_syntax_validity(self):
        """Проверка корректности синтаксиса Python для всех файлов"""
        for file_path in self.python_files:
            if file_path.exists():
                with self.subTest(file=str(file_path)):
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            source_code = f.read()
                        
                        # Проверяем синтаксис с помощью ast.parse
                        ast.parse(source_code, filename=str(file_path))
                        
                    except SyntaxError as e:
                        self.fail(f"Синтаксическая ошибка в {file_path}: {e}")
                    except UnicodeDecodeError as e:
                        self.fail(f"Ошибка кодировки в {file_path}: {e}")
    
    def test_python_compilation(self):
        """Проверка компиляции Python файлов"""
        for file_path in self.python_files:
            if file_path.exists() and file_path.suffix == '.py':
                with self.subTest(file=str(file_path)):
                    try:
                        py_compile.compile(str(file_path), doraise=True)
                    except py_compile.PyCompileError as e:
                        self.fail(f"Ошибка компиляции {file_path}: {e}")
    
    def test_import_statements(self):
        """Проверка корректности import statements"""
        main_app_file = self.project_root / 'streamlit_app.py'
        
        if main_app_file.exists():
            try:
                with open(main_app_file, 'r', encoding='utf-8') as f:
                    source_code = f.read()
                
                tree = ast.parse(source_code)
                
                # Собираем все импорты
                imports = []
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            imports.append(alias.name)
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            imports.append(node.module)
                
                # Проверяем, что основные библиотеки импортированы
                expected_imports = ['pandas', 'matplotlib', 'streamlit']
                for expected in expected_imports:
                    found = any(expected in imp for imp in imports)
                    self.assertTrue(found, f"Не найден импорт библиотеки: {expected}")
                    
            except Exception as e:
                self.fail(f"Ошибка анализа импортов: {e}")
    
    def test_function_definitions(self):
        """Проверка определений функций"""
        main_app_file = self.project_root / 'streamlit_app.py'
        
        if main_app_file.exists():
            try:
                with open(main_app_file, 'r', encoding='utf-8') as f:
                    source_code = f.read()
                
                tree = ast.parse(source_code)
                
                # Находим все функции
                functions = []
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        functions.append(node.name)
                
                # Проверяем наличие основных функций
                expected_functions = ['analyze_sales_data', 'create_visualizations', 'main']
                for func_name in expected_functions:
                    self.assertIn(func_name, functions, f"Функция {func_name} не найдена")
                
                # Проверяем, что функции не пустые
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        self.assertTrue(len(node.body) > 0, f"Функция {node.name} пустая")
                        
            except Exception as e:
                self.fail(f"Ошибка анализа функций: {e}")
    
    def test_docstrings_presence(self):
        """Проверка наличия docstrings"""
        main_app_file = self.project_root / 'streamlit_app.py'
        
        if main_app_file.exists():
            try:
                with open(main_app_file, 'r', encoding='utf-8') as f:
                    source_code = f.read()
                
                tree = ast.parse(source_code)
                
                # Проверяем docstring модуля
                if (tree.body and isinstance(tree.body[0], ast.Expr) and 
                    isinstance(tree.body[0].value, ast.Constant) and
                    isinstance(tree.body[0].value.value, str)):
                    module_docstring = tree.body[0].value.value
                    self.assertTrue(len(module_docstring) > 10, "Docstring модуля слишком короткий")
                
                # Проверяем docstrings функций
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        if (node.body and isinstance(node.body[0], ast.Expr) and
                            isinstance(node.body[0].value, ast.Constant) and
                            isinstance(node.body[0].value.value, str)):
                            func_docstring = node.body[0].value.value
                            self.assertTrue(len(func_docstring) > 5, 
                                          f"Docstring функции {node.name} слишком короткий")
                        else:
                            # Предупреждение для функций без docstring
                            print(f"Предупреждение: функция {node.name} не имеет docstring")
                            
            except Exception as e:
                self.fail(f"Ошибка анализа docstrings: {e}")


class TestCodeStructure(unittest.TestCase):
    """Тесты структуры кода"""
    
    def setUp(self):
        """Настройка"""
        self.project_root = Path(__file__).parent.parent
        self.main_app_file = self.project_root / 'streamlit_app.py'
    
    def test_main_function_exists(self):
        """Проверка наличия main функции"""
        if self.main_app_file.exists():
            with open(self.main_app_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.assertIn('def main()', content, "Функция main() не найдена")
            self.assertIn('if __name__ == "__main__":', content, 
                         "Блок if __name__ == '__main__' не найден")
    
    def test_error_handling(self):
        """Проверка обработки ошибок"""
        if self.main_app_file.exists():
            with open(self.main_app_file, 'r', encoding='utf-8') as f:
                source_code = f.read()
            
            tree = ast.parse(source_code)
            
            # Проверяем наличие try-except блоков
            try_except_found = False
            for node in ast.walk(tree):
                if isinstance(node, ast.Try):
                    try_except_found = True
                    # Проверяем, что есть обработчики исключений
                    self.assertTrue(len(node.handlers) > 0, "Try блок без except обработчиков")
            
            self.assertTrue(try_except_found, "Не найдено обработки исключений (try-except)")
    
    def test_variable_naming_conventions(self):
        """Проверка соглашений именования переменных"""
        if self.main_app_file.exists():
            with open(self.main_app_file, 'r', encoding='utf-8') as f:
                source_code = f.read()
            
            tree = ast.parse(source_code)
            
            # Проверяем именование функций (snake_case)
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    func_name = node.name
                    if not func_name.startswith('_'):  # Игнорируем приватные функции
                        self.assertTrue(func_name.islower() or '_' in func_name,
                                      f"Функция {func_name} не соответствует snake_case")
    
    def test_code_complexity(self):
        """Базовая проверка сложности кода"""
        if self.main_app_file.exists():
            with open(self.main_app_file, 'r', encoding='utf-8') as f:
                source_code = f.read()
            
            tree = ast.parse(source_code)
            
            # Проверяем длину функций
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    # Подсчитываем количество строк в функции
                    if hasattr(node, 'lineno') and hasattr(node, 'end_lineno'):
                        lines_count = node.end_lineno - node.lineno
                        if lines_count > 100:  # Предупреждение для очень длинных функций
                            print(f"Предупреждение: функция {node.name} очень длинная ({lines_count} строк)")


class TestCodeSecurity(unittest.TestCase):
    """Тесты безопасности кода"""
    
    def setUp(self):
        """Настройка"""
        self.project_root = Path(__file__).parent.parent
        self.python_files = list(self.project_root.glob('*.py'))
        self.python_files.extend(list((self.project_root / 'tests').glob('*.py')))
        self.python_files.extend(list((self.project_root / 'docs').glob('*.py')))
    
    def test_no_hardcoded_secrets(self):
        """Проверка на отсутствие захардкоженных секретов"""
        suspicious_patterns = [
            'password', 'secret', 'api_key', 'token', 'private_key'
        ]
        
        for file_path in self.python_files:
            if file_path.exists():
                with self.subTest(file=str(file_path)):
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read().lower()
                        
                        for pattern in suspicious_patterns:
                            if pattern in content:
                                # Проверяем, что это не просто строка в комментарии или docstring
                                lines = content.split('\n')
                                for i, line in enumerate(lines):
                                    if pattern in line and '=' in line and not line.strip().startswith('#'):
                                        print(f"Предупреждение: возможный секрет в {file_path}:{i+1}")
                                        
                    except UnicodeDecodeError:
                        pass  # Игнорируем бинарные файлы
    
    def test_no_dangerous_imports(self):
        """Проверка на опасные импорты"""
        dangerous_modules = ['subprocess', 'os.system', 'eval', 'exec']
        
        for file_path in self.python_files:
            if file_path.exists() and file_path.suffix == '.py':
                with self.subTest(file=str(file_path)):
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            source_code = f.read()
                        
                        tree = ast.parse(source_code)
                        
                        for node in ast.walk(tree):
                            if isinstance(node, ast.Import):
                                for alias in node.names:
                                    if alias.name in dangerous_modules:
                                        print(f"Предупреждение: опасный импорт {alias.name} в {file_path}")
                            elif isinstance(node, ast.ImportFrom):
                                if node.module and node.module in dangerous_modules:
                                    print(f"Предупреждение: опасный импорт {node.module} в {file_path}")
                                    
                    except Exception:
                        pass  # Игнорируем ошибки парсинга
    
    def test_file_operations_safety(self):
        """Проверка безопасности файловых операций"""
        if self.project_root / 'streamlit_app.py' in self.python_files:
            main_file = self.project_root / 'streamlit_app.py'
            
            try:
                with open(main_file, 'r', encoding='utf-8') as f:
                    source_code = f.read()
                
                tree = ast.parse(source_code)
                
                # Проверяем использование open() с небезопасными режимами
                for node in ast.walk(tree):
                    if isinstance(node, ast.Call):
                        if (isinstance(node.func, ast.Name) and node.func.id == 'open'):
                            # Проверяем аргументы open()
                            if len(node.args) > 1:
                                mode_arg = node.args[1]
                                if (isinstance(mode_arg, ast.Constant) and 
                                    isinstance(mode_arg.value, str) and 
                                    'w' in mode_arg.value):
                                    print(f"Предупреждение: запись в файл обнаружена в {main_file}")
                                    
            except Exception:
                pass


class TestCodeMetrics(unittest.TestCase):
    """Тесты метрик кода"""
    
    def setUp(self):
        """Настройка"""
        self.project_root = Path(__file__).parent.parent
        self.main_app_file = self.project_root / 'streamlit_app.py'
    
    def test_file_size(self):
        """Проверка размера файлов"""
        if self.main_app_file.exists():
            file_size = self.main_app_file.stat().st_size
            # Предупреждение для очень больших файлов (> 50KB)
            if file_size > 50000:
                print(f"Предупреждение: файл {self.main_app_file.name} очень большой ({file_size} байт)")
            
            # Проверяем, что файл не пустой
            self.assertGreater(file_size, 100, "Главный файл приложения слишком мал")
    
    def test_lines_of_code(self):
        """Подсчет строк кода"""
        if self.main_app_file.exists():
            with open(self.main_app_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            total_lines = len(lines)
            blank_lines = sum(1 for line in lines if line.strip() == '')
            comment_lines = sum(1 for line in lines if line.strip().startswith('#'))
            code_lines = total_lines - blank_lines - comment_lines
            
            print(f"Статистика {self.main_app_file.name}:")
            print(f"  Всего строк: {total_lines}")
            print(f"  Пустых строк: {blank_lines}")
            print(f"  Комментариев: {comment_lines}")
            print(f"  Строк кода: {code_lines}")
            
            # Проверяем минимальное количество строк кода
            self.assertGreater(code_lines, 50, "Слишком мало строк кода")
    
    def test_function_count(self):
        """Подсчет количества функций"""
        if self.main_app_file.exists():
            with open(self.main_app_file, 'r', encoding='utf-8') as f:
                source_code = f.read()
            
            tree = ast.parse(source_code)
            
            functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
            function_count = len(functions)
            
            print(f"Найдено функций: {function_count}")
            print(f"Список функций: {functions}")
            
            # Проверяем минимальное количество функций
            self.assertGreater(function_count, 2, "Слишком мало функций в приложении")


if __name__ == '__main__':
    # Запуск тестов качества кода
    unittest.main(verbosity=2)