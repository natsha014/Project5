# Используем готовый образ с Python
FROM python:3.13-slim

# Эти настройки сделают работу в Docker стабильнее
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false

# Устанавливаем системные зависимости (для базы и скачивания Poetry)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Poetry
RUN pip install poetry

# Рабочая папка
WORKDIR /code

# Копируем файлы зависимостей
COPY pyproject.toml poetry.lock* ./

# Устанавливаем зависимости проекта
RUN poetry install --no-root

# Копируем остальной код проекта
COPY . .

# Открываем порт для Django
EXPOSE 8000

# Определяем команду для запуска приложения
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
