from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from alembic import command
from alembic.config import Config
from backend.app.core.settings import settings

# ---------------------------
# ⚙️ Параметры подключения
# ---------------------------

# 🔽 Адрес базы данных
# Пример для SQLite (тестовая локальная база), позже можно заменить на PostgreSQL или MySQL
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# ---------------------------
# 🚀 Создание движка БД
# ---------------------------
# Создаем движок SQLAlchemy, который будет управлять подключением к базе данных
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# ---------------------------
# 🧠 Создание фабрики сессий
# ---------------------------
# Создаем фабрику сессий, которая будет генерировать сессии для работы с БД
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# ---------------------------
# 📦 Базовый класс для моделей
# ---------------------------
# Создаем базовый класс для моделей SQLAlchemy
Base = declarative_base()

# Функция для получения сессии БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
