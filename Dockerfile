# 1. Используем готовый образ с Python
FROM python:3.13-slim

# 2. Устанавливаем системные зависимости (для базы и скачивания Poetry)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 3. Устанавливаем Poetry
RUN pip install poetry

# 4. Рабочая папка
WORKDIR /code

# 5. Копируем файлы зависимостей
COPY pyproject.toml poetry.lock* ./

# Устанавливаем зависимости проекта
RUN poetry install --no-root

# 7. Копируем остальной код проекта
COPY . .

# 8. Открываем порт для Django
EXPOSE 8000

# Определяем команду для запуска приложения
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
