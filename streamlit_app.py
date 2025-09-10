# -*- coding: utf-8 -*-
"""
Streamlit приложение для анализа данных о продажах
Основано на анализе из пример1.py
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
from datetime import datetime

# Настройка страницы
st.set_page_config(
    page_title="Анализ данных о продажах",
    page_icon="📊",
    layout="wide"
)

def analyze_sales_data(df):
    """Функция для анализа данных о продажах"""
    results = {}
    
    # Обработка первого столбца как даты
    if df.columns[0] == 'Unnamed: 0' or 'дата' in df.columns[0].lower():
        df.iloc[:, 0] = pd.to_datetime(df.iloc[:, 0])
        df = df.set_index(df.columns[0])
    
    # Базовая статистика
    results['basic_stats'] = df.describe()
    
    # Общие продажи по продуктам
    results['total_sales_per_product'] = df.sum()
    
    # Общие ежемесячные продажи
    results['total_monthly_sales'] = df.sum(axis=1)
    
    # Средние ежемесячные продажи по продуктам
    results['average_monthly_sales_per_product'] = df.mean()
    
    # Месяц с наивысшими продажами
    results['month_highest_sales'] = results['total_monthly_sales'].idxmax()
    
    # Продукт с наивысшими общими продажами
    results['product_highest_sales'] = results['total_sales_per_product'].idxmax()
    
    return results, df

def create_visualizations(df, results):
    """Создание визуализаций"""
    
    # График общих ежемесячных продаж
    fig1, ax1 = plt.subplots(figsize=(12, 6))
    ax1.plot(results['total_monthly_sales'].index, results['total_monthly_sales'].values, marker='o')
    ax1.set_title('Общие ежемесячные продажи', fontsize=16, fontweight='bold')
    ax1.set_xlabel('Дата')
    ax1.set_ylabel('Общие продажи')
    ax1.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # График общих продаж по продуктам
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    bars = ax2.bar(results['total_sales_per_product'].index, results['total_sales_per_product'].values, color='skyblue')
    ax2.set_title('Общие продажи по продуктам', fontsize=16, fontweight='bold')
    ax2.set_xlabel('Продукт')
    ax2.set_ylabel('Общие продажи')
    
    # Добавление значений на столбцы
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height):,}',
                ha='center', va='bottom')
    
    plt.tight_layout()
    
    # Тепловая карта корреляций
    fig3, ax3 = plt.subplots(figsize=(8, 6))
    correlation_matrix = df.corr()
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, ax=ax3)
    ax3.set_title('Корреляция между продуктами', fontsize=16, fontweight='bold')
    plt.tight_layout()
    
    return fig1, fig2, fig3

def main():
    st.title("📊 Анализ данных о продажах")
    st.markdown("---")
    
    # Боковая панель для загрузки файла
    st.sidebar.header("Загрузка данных")
    
    # Загрузка примера данных
    if st.sidebar.button("Использовать пример данных"):
        try:
            example_df = pd.read_excel('docs/sample_sales_data.xlsx')
            st.session_state['uploaded_data'] = example_df
            st.sidebar.success("Пример данных загружен!")
        except FileNotFoundError:
            st.sidebar.error("Пример файла не найден в папке docs/")
    
    # Загрузка пользовательского файла
    uploaded_file = st.sidebar.file_uploader(
        "Выберите Excel файл",
        type=['xlsx', 'xls'],
        help="Загрузите Excel файл с данными о продажах"
    )
    
    if uploaded_file is not None:
        try:
            df = pd.read_excel(uploaded_file)
            st.session_state['uploaded_data'] = df
            st.sidebar.success("Файл успешно загружен!")
        except Exception as e:
            st.sidebar.error(f"Ошибка загрузки файла: {e}")
    
    # Основной анализ
    if 'uploaded_data' in st.session_state:
        df = st.session_state['uploaded_data']
        
        # Отображение базовой информации о данных
        st.header("1. 📋 Обзор данных")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Количество строк", df.shape[0])
        with col2:
            st.metric("Количество столбцов", df.shape[1])
        with col3:
            st.metric("Пропущенные значения", df.isnull().sum().sum())
        
        # Показать первые несколько строк
        st.subheader("Первые 5 строк данных:")
        st.dataframe(df.head())
        
        # Информация о типах данных
        st.subheader("Информация о столбцах:")
        buffer = io.StringIO()
        df.info(buf=buffer)
        info_str = buffer.getvalue()
        st.text(info_str)
        
        # Проведение анализа
        try:
            results, processed_df = analyze_sales_data(df.copy())
            
            # Статистический анализ
            st.header("2. 📊 Статистический анализ")
            st.subheader("Описательная статистика:")
            st.dataframe(results['basic_stats'])
            
            # Ключевые показатели
            st.header("3. 🎯 Ключевые показатели")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Общие продажи по продуктам:")
                st.dataframe(results['total_sales_per_product'])
                
                st.subheader("Средние ежемесячные продажи:")
                st.dataframe(results['average_monthly_sales_per_product'])
            
            with col2:
                st.subheader("Топ показатели:")
                st.write(f"**Продукт с наивысшими продажами:** {results['product_highest_sales']}")
                if hasattr(results['month_highest_sales'], 'strftime'):
                    st.write(f"**Месяц с наивысшими продажами:** {results['month_highest_sales'].strftime('%Y-%m-%d')}")
                else:
                    st.write(f"**Период с наивысшими продажами:** {results['month_highest_sales']}")
                
                # Топ 3 продукта
                top_products = results['total_sales_per_product'].nlargest(3)
                st.subheader("Топ 3 продукта:")
                for i, (product, sales) in enumerate(top_products.items(), 1):
                    st.write(f"{i}. {product}: {sales:,.0f}")
            
            # Визуализации
            st.header("4. 📈 Визуализация данных")
            
            try:
                fig1, fig2, fig3 = create_visualizations(processed_df, results)
                
                # График временных рядов
                st.subheader("Динамика общих продаж:")
                st.pyplot(fig1)
                
                # График по продуктам
                st.subheader("Сравнение продуктов:")
                st.pyplot(fig2)
                
                # Корреляционная матрица
                st.subheader("Корреляция между продуктами:")
                st.pyplot(fig3)
                
                plt.close('all')  # Закрыть все фигуры для освобождения памяти
                
            except Exception as e:
                st.error(f"Ошибка создания графиков: {e}")
            
            # Отчет
            st.header("5. 📝 Итоговый отчет")
            
            report = f"""
            ## Отчет по анализу данных о продажах
            
            ### Основные результаты:
            - **Общее количество записей:** {df.shape[0]}
            - **Количество продуктов:** {df.shape[1] - 1}
            - **Лучший продукт:** {results['product_highest_sales']} 
              (общие продажи: {results['total_sales_per_product'][results['product_highest_sales']]:,.0f})
            - **Средние продажи за период:** {results['total_monthly_sales'].mean():,.0f}
            - **Максимальные продажи за месяц:** {results['total_monthly_sales'].max():,.0f}
            - **Минимальные продажи за месяц:** {results['total_monthly_sales'].min():,.0f}
            
            ### Выводы:
            - Продажи показывают {'восходящий' if results['total_monthly_sales'].iloc[-1] > results['total_monthly_sales'].iloc[0] else 'нисходящий'} тренд
            - Наибольшая корреляция наблюдается между продуктами с коэффициентом {processed_df.corr().values[processed_df.corr().values != 1].max():.3f}
            - Стандартное отклонение общих продаж: {results['total_monthly_sales'].std():,.0f}
            
            ### Использованные библиотеки:
            - **pandas**: Обработка и анализ данных
            - **matplotlib**: Визуализация данных
            - **seaborn**: Статистическая визуализация
            - **streamlit**: Веб-интерфейс приложения
            """
            
            st.markdown(report)
            
            # Кнопка для скачивания отчета
            st.download_button(
                label="📥 Скачать отчет (TXT)",
                data=report,
                file_name=f"sales_analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )
            
        except Exception as e:
            st.error(f"Ошибка анализа данных: {e}")
            st.info("Убедитесь, что ваш файл содержит данные в правильном формате.")
    
    else:
        st.info("👆 Пожалуйста, загрузите Excel файл для начала анализа")
        
        # Показать пример структуры данных
        st.subheader("Ожидаемая структура данных:")
        example_structure = pd.DataFrame({
            'Дата': ['2020-01-01', '2020-02-01', '2020-03-01'],
            'Продукт_1': [1000, 1200, 1100],
            'Продукт_2': [1500, 1300, 1400],
            'Продукт_3': [800, 900, 850]
        })
        st.dataframe(example_structure)

if __name__ == "__main__":
    main()