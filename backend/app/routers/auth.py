from datetime import timedelta
from typing import Dict, Optional, Union
from fastapi import APIRouter, Body, Depends, Form, HTTPException, Response, status
from fastapi.responses import JSONResponse
from backend.app.core.dependencies import get_db
from backend.app.schemas.user import UserBase, UserWithWorkshops
from backend.app.middlewares.auth_middleware import create_auth_token, decode_auth_token, verify_password
from backend.app.services import user_service
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordBearer
from backend.app.core.settings import settings

router = APIRouter()
# В зависимости от того, где вам нужно проверять токен
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/login", summary="Авторизация пользователя")
async def login_api(
    username: str = Body(...),
    password: str = Body(...),
    db: AsyncSession = Depends(get_db)
):
    """Аутентификация пользователя, возвращает access токен"""
    user = await user_service.get_user_by_username(db, username)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль"
        )

    if not await verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль"
        )

    auth_token = create_auth_token({"sub": user.username, "user_id": user.id})
    return JSONResponse(content={
        "auth_token": auth_token,
        "token_type": "bearer",
        "user": UserWithWorkshops.model_validate(user).model_dump()
    })


@router.post("/logout", summary="Выход из аккаунта")
async def logout_api():
    response = JSONResponse(
        content={"message": "Вы успешно вышли из системы."},
        status_code=status.HTTP_200_OK
    )
    # Удаляем куку с токеном — max_age=0 или expires на прошедшую дату
    response.delete_cookie(key="auth_token")
    return response

@router.post("/token")
async def login_for_auth_token(response: Response, username: str = Form(...), password: str = Form(...), db: AsyncSession = Depends(get_db)):
    from services.user_service import get_user_by_username
    user = await get_user_by_username(db, username)
    if not user or not await verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    # Генерация токена с помощью create_auth_token
    payload = {"user_id": user.id}
    token = create_auth_token(payload, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))

    return {"auth_token": token, "token_type": "bearer"}

@router.get("/validate_token")
async def validate_token(token: str = Depends(oauth2_scheme)) -> Dict[str, Optional[Union[str, int, bool]]]:
    try:
        payload = decode_auth_token(token)  # если decode_auth_token не async, await не нужен
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if payload:
        return {
            "valid": True,
            "user_id": payload.get("user_id"),
            "username": payload.get("sub")
        }
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )