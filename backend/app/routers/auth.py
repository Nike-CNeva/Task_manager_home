from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from backend.app.core.dependencies import get_db
from backend.app.schemas.user import UserBase
from middlewares.auth_middleware import create_access_token, verify_password
from services import user_service
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

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

    access_token = create_access_token({"sub": user.username, "user_id": user.id})
    return JSONResponse(content={
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserBase.model_validate(user).model_dump()
    })


@router.post("/logout", summary="Выход из аккаунта")
async def logout_api():
    response = JSONResponse(
        content={"message": "Вы успешно вышли из системы."},
        status_code=status.HTTP_200_OK
    )
    # Удаляем куку с токеном — max_age=0 или expires на прошедшую дату
    response.delete_cookie(key="access_token")
    return response