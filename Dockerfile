# Быстрый Docker образ для локальной разработки
FROM python:3.13-slim

WORKDIR /app

# Устанавливаем только минимально необходимые системные пакеты
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Копируем requirements и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем приложение
COPY streamlit_app.py .

# Открываем порт
EXPOSE 8501

# Запуск приложения
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]