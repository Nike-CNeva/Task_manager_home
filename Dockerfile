# Этап 1 — Сборка фронтенда (Vue)
FROM node:20 AS frontend-builder
WORKDIR /app/frontend
COPY frontend/ ./

# Добавим переменные окружения во время сборки для продакшн
#COPY frontend/.env.production .env.production

RUN npm install && npm run build

# Этап 2 — Бэкенд (FastAPI)
FROM python:3.11-slim AS backend

WORKDIR /app

# Установка зависимостей
COPY backend/requirements.txt ./backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt

# Копируем backend-код
COPY backend/ ./backend/

# Копируем сборку фронта в статическую папку для продакшн
#COPY --from=frontend-builder /app/frontend/dist ./backend/app/static

ENV PYTHONPATH=/app/backend

CMD ["uvicorn", "backend.app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
