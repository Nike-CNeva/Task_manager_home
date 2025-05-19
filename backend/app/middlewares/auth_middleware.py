from datetime import datetime, timedelta, timezone
import logging
from typing import Any, Awaitable, Callable, Dict, Optional
from jose import ExpiredSignatureError, jwt, JWTError
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import APIRouter, Request, Response
from passlib.context import CryptContext
from backend.app.core.settings import settings


router = APIRouter()

# Инициализация хэширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


logger = logging.getLogger("auth_middleware")

PUBLIC_PATHS = {"/", "/login", "/docs", "/redoc", "/openapi.json"}

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        path = request.url.path

        # Если маршрут не начинается с /api — пропускаем проверку авторизации
        if not path.startswith("/api"):
            return await call_next(request)

        # Далее проверяем публичные пути в /api, которые не требуют авторизации
        if path in PUBLIC_PATHS:
            return await call_next(request)
        
        auth_header = request.headers.get("Authorization")
        token_part = None

        if not auth_header:
            logger.warning("❌ Токен не передан, доступ запрещён")
            request.state.user_id = None
            return Response("Unauthorized", status_code=401)

        if not auth_header.startswith("Bearer "):
            logger.warning("❌ Неверный формат токена, ожидается 'Bearer <token>'")
            request.state.user_id = None
            return await call_next(request)

        token_part = auth_header[len("Bearer "):]
        logger.debug(f"🔐 Получен auth_token: {auth_header}")
        logger.debug(f"🧩 Token part: {token_part}")

        try:
            payload = decode_auth_token(token_part)
            logger.debug(f"📦 Распакованный payload: {payload}")
            if payload:
                request.state.user_id = payload.get("user_id")
                # Добавляем логирование оставшегося времени токена
                exp_timestamp = payload.get("exp")
                if exp_timestamp:
                    now = datetime.now(timezone.utc).timestamp()
                    remaining = exp_timestamp - now
                    if remaining > 0:
                        logger.info(f"⏳ Остаток времени жизни токена: {remaining:.2f} секунд")
                    else:
                        logger.warning("❌ Токен просрочен!")
                else:
                    logger.warning("⚠️ В payload нет поля 'exp'")

            else:
                logger.warning("❌ Payload пустой")
                request.state.user_id = None
        except JWTError as e:
            logger.warning(f"❌ Ошибка JWT: {e}")
            request.state.user_id = None

        if request.state.user_id is None and request.url.path not in {"/", "/login"}:
            return Response("Unauthorized", status_code=401)

        logger.info(f"🔍 Middleware получил запрос: {request.url}")

        try:
            response = await call_next(request)
        except Exception as e:
            logger.error(f"❌ Ошибка в обработчике запроса: {e}")
            response = Response("Ошибка сервера", status_code=500)

        logger.info(f"✅ Middleware пропустил запрос: {request.url}")

        return response

# ================================
# Хэширование и проверка пароля
# ================================
async def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет соответствие хэшированного пароля введенному."""
    return pwd_context.verify(plain_password, hashed_password)

async def get_password_hash(password: str) -> str:
    """Хэширует пароль перед сохранением в БД."""
    return pwd_context.hash(password)

# ================================
# Генерация и проверка JWT токенов
# ================================
def create_auth_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Создает JWT-токен с заданным сроком действия.
    :param data: Данные для кодирования в токен
    :param expires_delta: Время жизни токена
    :return: Закодированный JWT-токен
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        
    return token


def decode_auth_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except ExpiredSignatureError:
        print("❌ Токен просрочен")
        return None
    except JWTError as e:
        print(f"❌ Ошибка при декодировании токена: {e}")
        return None

