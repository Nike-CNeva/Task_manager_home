from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import async_sessionmaker
from backend.app.core.settings import settings

# ---------------------------
# ⚙️ Параметры подключения
# ---------------------------
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL  # Убедитесь, что используете правильный URL для асинхронного подключения

# ---------------------------
# 🚀 Создание асинхронного движка БД
# ---------------------------
# Используем create_async_engine для асинхронного подключения
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# ---------------------------
# 🧠 Создание фабрики асинхронных сессий
# ---------------------------
# Здесь используем AsyncSession для работы с асинхронной сессией
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,  # Указываем, что сессии должны быть асинхронными
    expire_on_commit=False
)

# ---------------------------
# 📦 Базовый класс для моделей
# ---------------------------
class Base(DeclarativeBase):
    pass

# Функция для получения асинхронной сессии БД
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session
