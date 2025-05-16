# Этап 1 — Сборка фронтенда
FROM node:20 AS frontend-builder

WORKDIR /app/frontend

COPY frontend/ ./

RUN npm install && npm run build

# Этап 2 — Бэкенд (FastAPI)
FROM python:3.11-slim AS backend

WORKDIR /app/backend

# Установка зависимостей Python
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Копируем backend-код
COPY backend/ ./

# Копируем билд фронта в static
COPY --from=frontend-builder /app/frontend/dist ./app/static

ENV PYTHONPATH=/app

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
