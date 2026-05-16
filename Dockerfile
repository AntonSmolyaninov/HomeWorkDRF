FROM python:3.12-slim

# Установка системных зависимостей (добавлено для psycopg2)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Установка Poetry
RUN pip install --no-cache-dir poetry

WORKDIR /app

# Копирование и установка зависимостей
COPY pyproject.toml poetry.lock* ./

# Создаем poetry.lock если нет
RUN if [ ! -f poetry.lock ]; then poetry lock; fi

# Установка зависимостей (убрал --no-root для совместимости)
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Копирование кода
COPY . .

# Создание директорий для статики и медиа
RUN mkdir -p staticfiles media

# Безопасность
RUN groupadd -r django && useradd -r -g django django
RUN chown -R django:django /app
USER django

EXPOSE 8000

# Healthcheck (добавлен curl, но он уже установлен выше)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl --fail http://localhost:8000/health/ || exit 1

# Запуск
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4", "--access-logfile", "-", "--error-logfile", "-"]
