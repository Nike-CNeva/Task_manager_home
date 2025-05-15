from datetime import datetime, timedelta
from typing import Dict, Optional
from fastapi.responses import RedirectResponse
from jose import jwt, JWTError
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import APIRouter, Form, Request, HTTPException, Response, status, Depends
from passlib.context import CryptContext
from backend.app.core.dependencies import get_db
from backend.app.core.settings import settings
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

router = APIRouter()

# Инициализация хэширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# В зависимости от того, где вам нужно проверять токен
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class AuthMiddleware(BaseHTTPMiddleware):
    """
    Middleware для проверки авторизации через JWT.
    """
    async def dispatch(self, request: Request, call_next):
        access_token = request.headers.get("Authorization")
        token_part = None
        
        if access_token:
            if access_token.startswith("Bearer "):
                token_part = access_token.split(" ", 1)[1]
            else:
                print("❌ Неверный формат токена, ожидается 'Bearer <token>'")
                request.state.user_id = None
                return await call_next(request)
        else:
            # Если нет токена, проверяем путь
            if request.url.path in ["/", "/login", "/docs", "/redoc", "/openapi.json"]:
                return await call_next(request)
            print("❌ Токен не передан, доступ запрещён")
            request.state.user_id = None
            return Response("Unauthorized", status_code=401)

        try:
            print(f"🔐 Получен access_token: {access_token}")
            print(f"🧩 Token part: {token_part}")
            payload = decode_access_token(token_part)  # Функция декодирования токена
            print(f"📦 Распакованный payload: {payload}")
            if payload:
                request.state.user_id = payload.get("user_id")
            else:
                print("❌ Payload пустой, возможно, decode_access_token() не сработал")
                request.state.user_id = None
        except JWTError as e:
            print(f"❌ Ошибка JWT: {e}")
            request.state.user_id = None

        # Проверяем, если нет user_id, и путь не /login, редиректим на страницу входа
        if request.state.user_id is None and request.url.path not in ["/", "/login"]:
            response = Response("Unauthorized", status_code=401)  # Можно настроить редирект или другое сообщение
            return response  # Возвращаем Response без `await`

        print(f"🔍 Middleware получил запрос: {request.url}")

        try:
            response = await call_next(request)  # Пропускаем запрос дальше
        except Exception as e:
            print(f"❌ Ошибка в обработчике запроса: {e}")
            response = Response("Ошибка сервера", status_code=500)

        print(f"✅ Middleware пропустил запрос: {request.url}")

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
def create_access_token(data: Dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Создает JWT-токен с заданным сроком действия.
    :param data: Данные для кодирования в токен
    :param expires_delta: Время жизни токена
    :return: Закодированный JWT-токен
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    
    # Вывод токена в консоль
    
    return token


def decode_access_token(token: str):
    """
    Декодирует JWT-токен и проверяет его корректность.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError as e:
        print(f"❌ Ошибка при декодировании токена: {e}")
        return None

# Функция для извлечения токена из cookies
def get_token_from_cookie(request: Request):
    token = request.cookies.get("access_token")  # Получаем токен из куки
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return token

@router.post("/token")
async def login_for_access_token(response: Response, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    from services.user_service import get_user_by_username
    user = get_user_by_username(db, username)
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    # Генерация токена с помощью create_access_token
    payload = {"user_id": user.id}
    token = create_access_token(payload, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    # Сохранение токена в куки
    response.set_cookie(key="access_token", value=token, httponly=True, max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES*60)
    return {"access_token": token, "token_type": "bearer"}

@router.get("/validate_token")
async def validate_token(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if payload:
        return {"valid": True, "user_id": payload.get("user_id"), "username": payload.get("sub")}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )