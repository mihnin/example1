# -*- coding: utf-8 -*-
"""
Скрипт для запуска всех тестов с различными конфигурациями
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(command, description):
    """Запуск команды с выводом результата"""
    print(f"\n{'='*60}")
    print(f"🔧 {description}")
    print(f"{'='*60}")
    print(f"Команда: {' '.join(command)}")
    print()
    
    try:
        result = subprocess.run(command, capture_output=True, text=True, cwd=Path(__file__).parent.parent)
        
        if result.stdout:
            print("STDOUT:")
            print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        if result.returncode == 0:
            print(f"✅ {description} - УСПЕШНО")
        else:
            print(f"❌ {description} - ОШИБКА (код: {result.returncode})")
        
        return result.returncode == 0
        
    except FileNotFoundError:
        print(f"❌ Команда не найдена: {command[0]}")
        return False
    except Exception as e:
        print(f"❌ Ошибка выполнения: {e}")
        return False


def main():
    """Основная функция запуска тестов"""
    print("🚀 Запуск комплексного тестирования приложения анализа данных")
    print(f"📁 Рабочая директория: {os.getcwd()}")
    print(f"🐍 Python версия: {sys.version}")
    
    # Проверяем наличие pytest
    try:
        import pytest
        print(f"✅ pytest найден: версия {pytest.__version__}")
    except ImportError:
        print("❌ pytest не установлен. Установка...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pytest"])
    
    results = []
    
    # 1. Базовые юнит-тесты
    success = run_command(
        [sys.executable, "-m", "pytest", "tests/test_analysis_functions.py", "-v"],
        "Юнит-тесты функций анализа"
    )
    results.append(("Юнит-тесты", success))
    
    # 2. Интеграционные тесты
    success = run_command(
        [sys.executable, "-m", "pytest", "tests/test_streamlit_integration.py", "-v"],
        "Интеграционные тесты Streamlit"
    )
    results.append(("Интеграционные тесты", success))
    
    # 3. Тесты качества кода
    success = run_command(
        [sys.executable, "-m", "pytest", "tests/test_code_quality.py", "-v"],
        "Тесты качества кода и синтаксиса"
    )
    results.append(("Качество кода", success))
    
    # 4. Тесты образцов данных
    success = run_command(
        [sys.executable, "-m", "pytest", "tests/test_data_samples.py", "-v"],
        "Тесты с различными образцами данных"
    )
    results.append(("Образцы данных", success))
    
    # 5. Быстрые тесты (исключая медленные)
    success = run_command(
        [sys.executable, "-m", "pytest", "tests/", "-v", "-m", "not slow"],
        "Быстрые тесты (без медленных)"
    )
    results.append(("Быстрые тесты", success))
    
    # 6. Тесты производительности (только если указано)
    if "--performance" in sys.argv:
        success = run_command(
            [sys.executable, "-m", "pytest", "tests/", "-v", "-m", "performance"],
            "Тесты производительности"
        )
        results.append(("Производительность", success))
    
    # 7. Полный набор тестов
    success = run_command(
        [sys.executable, "-m", "pytest", "tests/", "-v", "--tb=short"],
        "Полный набор тестов"
    )
    results.append(("Полный набор", success))
    
    # 8. Тесты с покрытием кода (если pytest-cov установлен)
    try:
        import pytest_cov
        success = run_command(
            [sys.executable, "-m", "pytest", "tests/", "--cov=streamlit_app", "--cov-report=term-missing"],
            "Тесты с анализом покрытия кода"
        )
        results.append(("Покрытие кода", success))
    except ImportError:
        print("ℹ️  pytest-cov не установлен, пропускаем анализ покрытия")
    
    # 9. Проверка синтаксиса основных файлов
    success = run_command(
        [sys.executable, "-m", "py_compile", "streamlit_app.py"],
        "Проверка компиляции главного файла"
    )
    results.append(("Компиляция", success))
    
    # 10. Линтинг (если flake8 установлен)
    try:
        subprocess.run([sys.executable, "-m", "flake8", "--version"], capture_output=True, check=True)
        success = run_command(
            [sys.executable, "-m", "flake8", "streamlit_app.py", "--max-line-length=100", "--ignore=E501,W503"],
            "Линтинг кода (flake8)"
        )
        results.append(("Линтинг", success))
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("ℹ️  flake8 не установлен, пропускаем линтинг")
    
    # Итоговый отчет
    print(f"\n{'='*60}")
    print("📊 ИТОГОВЫЙ ОТЧЕТ ТЕСТИРОВАНИЯ")
    print(f"{'='*60}")
    
    total_tests = len(results)
    passed_tests = sum(1 for _, success in results if success)
    failed_tests = total_tests - passed_tests
    
    for test_name, success in results:
        status = "✅ ПРОЙДЕН" if success else "❌ ПРОВАЛЕН"
        print(f"  {test_name:<25} {status}")
    
    print(f"\n📈 Статистика:")
    print(f"  Всего тестов: {total_tests}")
    print(f"  Пройдено: {passed_tests}")
    print(f"  Провалено: {failed_tests}")
    print(f"  Успешность: {(passed_tests/total_tests)*100:.1f}%")
    
    if failed_tests == 0:
        print(f"\n🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
        return 0
    else:
        print(f"\n⚠️  НЕКОТОРЫЕ ТЕСТЫ ПРОВАЛИЛИСЬ")
        print(f"   Проверьте детали выше для исправления ошибок")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)