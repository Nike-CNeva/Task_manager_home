from fastapi import APIRouter, Body, Depends, Form, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from dependencies import get_db
from middlewares.auth_middleware import create_access_token, verify_password
from schemas import UserBase
from services import user_service

router = APIRouter()

@router.post("/login", summary="Авторизация пользователя")
def login_api(
    username: str = Body(...),
    password: str = Body(...),
    db: Session = Depends(get_db)
):
    """Аутентификация пользователя, возвращает access токен"""
    user = user_service.get_user_by_username(db, username)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль"
        )

    if not verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль"
        )

    access_token = create_access_token({"sub": user.username, "user_id": user.id})
    return JSONResponse(content={
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserBase.from_orm(user).dict()
    })

@router.post("/logout", summary="Выход из аккаунта")
def logout_api():
    """Сообщение об успешном выходе (токен удаляется на клиенте)"""
    return JSONResponse(
        content={"message": "Вы успешно вышли из системы."},
        status_code=status.HTTP_200_OK
    )
