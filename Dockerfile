# Используем официальный Python образ
FROM python:3.13-slim

# Устанавливаем метаданные
LABEL maintainer="Your Name <your.email@example.com>"
LABEL description="Streamlit приложение для анализа данных о продажах"
LABEL version="1.0.0"

# Устанавливаем рабочую директорию
WORKDIR /app

# Создаем пользователя для безопасности (не root)
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Копируем файл requirements.txt первым для лучшего кэширования Docker слоев
COPY requirements.txt .

# Устанавливаем Python зависимости
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копируем исходный код приложения
COPY streamlit_app.py .

# Создаем директорию docs и копируем только пример данных
RUN mkdir -p docs
COPY docs/sample_sales_data.xlsx ./docs/

# Создаем директории для данных
RUN mkdir -p /app/data /app/logs

# Настраиваем права доступа
RUN chown -R appuser:appuser /app
USER appuser

# Открываем порт для Streamlit
EXPOSE 8501

# Настройки Streamlit
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_ENABLE_CORS=false
ENV STREAMLIT_SERVER_ENABLE_XSRF_PROTECTION=false

# Проверка здоровья контейнера
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Команда запуска приложения
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]