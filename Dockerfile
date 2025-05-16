# --- Сборка фронтенда ---
FROM node:18 AS frontend

WORKDIR /app/frontend
COPY frontend/ /app/frontend/
RUN npm install && npm run build

# --- Сборка Python-бэкенда ---
FROM python:3.11 AS backend

# Устанавливаем зависимости
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код
COPY backend/ /app/backend
COPY --from=frontend /app/frontend/dist /app/backend/static

# Указываем рабочую директорию и команду запуска
WORKDIR /app/backend
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]