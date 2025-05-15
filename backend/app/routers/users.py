from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy import select
from backend.app.core.dependencies import get_current_user
from backend.app.database.database import get_db
from backend.app.models.enums import UserTypeEnum
from backend.app.schemas.user import PasswordChangeRequest, UserRead, UserSaveForm, UserWithWorkshops
from sqlalchemy.ext.asyncio import AsyncSession
from middlewares.auth_middleware import get_password_hash, verify_password
from backend.app.models.user import User
from backend.app.models.workshop import Workshop, WorkshopEnum
from services import user_service



router = APIRouter()

@router.get("/admin/users", response_model=List[UserWithWorkshops])
async def admin_users(db: AsyncSession = Depends(get_db), current_user: UserRead = Depends(get_current_user)):
    if current_user.user_type != UserTypeEnum.ADMIN:
        raise HTTPException(status_code=403, detail="Доступ запрещён")
        
    users = await user_service.get_users(db)
    users_with_workshops = [
        UserWithWorkshops(
            id=user.id,
            name=user.name,
            firstname=user.firstname,
            username=user.username,
            email=user.email,
            telegram=user.telegram,
            user_type=user.user_type.value,
            workshops=[workshop.name for workshop in user.workshops]
        )
        for user in users
    ]

    return users_with_workshops


@router.get("/admin/users/create", response_model=dict)
async def create_user_form(current_user: User = Depends(get_current_user)):
    if current_user.user_type != UserTypeEnum.ADMIN:
        raise HTTPException(status_code=403, detail="Доступ запрещён")
    workshops = [workshop.value for workshop in WorkshopEnum]
    roles = [role.value for role in UserTypeEnum]
    return JSONResponse(content={
        "roles": roles,
        "workshops": workshops
    })

@router.get("/admin/workshops", response_model=List[str])
async def get_workshops(current_user: User = Depends(get_current_user)):
    if current_user.user_type != UserTypeEnum.ADMIN:
        raise HTTPException(status_code=403, detail="Доступ запрещён")
    return [workshop.value for workshop in WorkshopEnum]

@router.post("/admin/users/save")
async def save_user(
    form_data: UserSaveForm,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.user_type != UserTypeEnum.ADMIN:
        raise HTTPException(status_code=403, detail="Доступ запрещён")

    # Преобразуем имена цехов в Enum
    try:
        workshop_enums = [WorkshopEnum(workshop) for workshop in form_data.workshops]
    except ValueError:
        raise HTTPException(status_code=400, detail="Некорректные цеха")

    # Получаем объекты цехов
    stmt = select(Workshop).where(Workshop.name.in_([w.value for w in workshop_enums]))
    result = await db.execute(stmt)
    workshop_objs = result.scalars().all()

    if not workshop_objs:
        raise HTTPException(status_code=400, detail="Цеха не найдены")

    try:
        if form_data.id:
            # Обновление пользователя
            await user_service.update_user(
                db=db,
                form_data=form_data,
                workshop_ids=[w.id for w in workshop_objs]
            )
            message = "Пользователь обновлён"
        else:
            # Создание нового пользователя
            await user_service.create_user(
                db=db,
                user_data=form_data,
                workshop_ids=[w.id for w in workshop_objs]
            )
            message = "Пользователь создан"

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при сохранении пользователя: {str(e)}")

    return JSONResponse(content={"message": message, "redirect_url": "/admin/users"})

@router.put("/admin/users/{user_id}/edit")
async def edit_user_form(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.user_type != UserTypeEnum.ADMIN:
        raise HTTPException(status_code=403, detail="Доступ запрещён")

    # Получаем пользователя
    user_select = select(User).where(User.id == user_id)
    result_user = await db.execute(user_select)
    user_obj: User | None = result_user.scalar_one_or_none()
    if not user_obj:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    # Получаем все цеха
    result_workshops = await db.execute(select(Workshop))
    workshops = result_workshops.scalars().all()

    roles = [role.value for role in UserTypeEnum]

    return JSONResponse(content={
        "roles": roles,
        "workshops": [w.name for w in workshops],
        "edit": True,
        "user_obj": {
            "id": user_obj.id,
            "name": user_obj.name,
            "firstname": user_obj.firstname,
            "username": user_obj.username,
            "email": user_obj.email,
            "user_type": user_obj.user_type.value
        },
        "user_workshops": [w.name for w in user_obj.workshops]
    })



@router.get("/profile")
async def get_profile(current_user: User = Depends(get_current_user)):
    print(f"Текущий пользователь: {current_user}")
    return JSONResponse(content={
        "user_authenticated": True,
        "name": current_user.name,
        "firstname": current_user.firstname,
        "email": current_user.email,
        "telegram": current_user.telegram,
        "username": current_user.username,
        "user_type": current_user.user_type.value,
        "tasks": [t.id for t in current_user.tasks],
        "workshops": [w.name for w in current_user.workshops],
        "comments": [c.id for c in current_user.comments],
    })


@router.put("/profile")
async def edit_profile(
    data: UserSaveForm,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Проверка email
    if data.email and data.email != current_user.email:
        user_email_check = select(User).where(User.email == data.email)
        result_email = await db.execute(user_email_check)
        user_with_email: User | None = result_email.scalar_one_or_none()
        if user_with_email:
            raise HTTPException(
                status_code=400,
                detail="Email уже используется другим пользователем"
            )

    # Проверка username
    if data.username != current_user.username:
        user_username_check = select(User).where(User.username == data.username)
        result_username = await db.execute(user_username_check)
        user_with_username: User | None = result_username.scalar_one_or_none()
        if user_with_username:
            raise HTTPException(
                status_code=400,
                detail="Username уже используется другим пользователем"
            )

    # Обновляем поля
    current_user.name = data.name
    current_user.firstname = str(data.firstname) if data.firstname else None # type: ignore
    current_user.username = data.username
    current_user.email = str(data.email) if data.email else None # type: ignore
    current_user.telegram = str(data.telegram) if data.telegram else None # type: ignore
    

    db.add(current_user)           # на всякий случай
    await db.commit()              # обязательно await
    await db.refresh(current_user)  # обновим объект после commit

    return JSONResponse(content={"message": "Профиль обновлён"})




@router.put("/profile/password")
async def change_password(
    data: PasswordChangeRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not await verify_password(data.current_password, current_user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Текущий пароль введен неверно"
        )
    
    if data.new_password != data.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Новый пароль и его подтверждение не совпадают"
        )

    current_user.password = await get_password_hash(data.new_password)
    db.add(current_user)  # добавляем в сессию, если не добавлен
    await db.commit()     # await нужен — это AsyncSession
    await db.refresh(current_user)

    return JSONResponse(
        content={"message": "Пароль успешно обновлён", "redirect_url": "/profile"}
    )