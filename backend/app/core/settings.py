from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):
    # Основные настройки приложения
    APP_NAME: str = "Система управления задачами"  # Название приложения
    DEBUG: bool

    # Пути к директориям
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    UPLOAD_DIR: Path = BASE_DIR / "uploads"

    # Настройки базы данных
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"  # Алгоритм для JWT
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # Время жизни токена доступа в минутах
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
# Создаем объект настроек
settings = Settings()
