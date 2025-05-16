FROM python:3.11-slim

WORKDIR /app/backend

# Копируем requirements из backend
COPY backend/requirements.txt ./ 

RUN pip install --no-cache-dir -r requirements.txt

# Копируем содержимое backend в /app/backend
COPY backend/ . 

ENV PYTHONPATH=/app

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
