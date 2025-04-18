from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    # Основные настройки приложения
    APP_NAME: str = "Система управления задачами"  # Название приложения
    DEBUG: bool = True  # Режим отладки

    # Пути к директориям
    BASE_DIR: Path = Path(__file__).parent.parent  # Базовая директория проекта
    UPLOAD_DIR: Path = Path("uploads")  # Директория для загрузки файлов

    # Настройки базы данных
    DATABASE_URL: str = "postgresql://postgres:Nike5427720@localhost/task_manager"  # URL для подключения к базе данных
    SECRET_KEY: str = "my_super_secret_key"  # Секретный ключ для JWT
    ALGORITHM: str = "HS256"  # Алгоритм для JWT
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # Время жизни токена доступа в минутах

    class Config:
        env_file = ".env"
        extra = "forbid"
        env_file_encoding = "utf-8"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Преобразуем BASE_DIR и UPLOAD_DIR в Path объекты
        self.BASE_DIR = Path(self.BASE_DIR).resolve()
        self.UPLOAD_DIR = self.BASE_DIR / self.UPLOAD_DIR
        
# Создаем объект настроек
settings = Settings()
