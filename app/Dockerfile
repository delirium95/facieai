FROM python:3.12-slim

# Встановлюємо Poetry
RUN pip install poetry

WORKDIR /app

# Копіюємо pyproject.toml і lock-файл
COPY ../pyproject.toml ../poetry.lock* ./

# Вимикаємо створення віртуального середовища (воно не потрібне в контейнері)
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

# Копіюємо весь код
COPY . .

EXPOSE 8000

# Запускаємо FastAPI
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
