from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from backend.app.core.dependencies import get_current_user, get_db
from backend.app.models.enums import UserTypeEnum
from backend.app.schemas.user import UserRead, UserSaveForm, UserWithWorkshops
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
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.user_type != UserTypeEnum.ADMIN:
        raise HTTPException(status_code=403, detail="Доступ запрещён")

    try:
        workshop_enums = [WorkshopEnum(workshop) for workshop in form_data.workshops]
    except ValueError:
        raise HTTPException(status_code=400, detail="Некорректные цеха")

    workshop_objs = db.query(Workshop).filter(Workshop.name.in_([w.value for w in workshop_enums])).all()

    if not workshop_objs:
        raise HTTPException(status_code=400, detail="Цеха не найдены")

    try:
        if form_data.id:  # редактирование
            user_service.update_user(
                db=db,
                form_data=form_data,
                workshop_ids=[w.id for w in workshop_objs]
            )
            message = "Пользователь обновлён"
        else:  # создание
            user_service.create_user(
                db,
                {
                    "name": form_data.name,
                    "firstname": form_data.firstname,
                    "username": form_data.username,
                    "user_type": form_data.user_type,
                    "password": form_data.password,
                },
                [w.id for w in workshop_objs]
            )
            message = "Пользователь создан"

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при сохранении пользователя: {str(e)}")

    return JSONResponse(content={"message": message, "redirect_url": "/admin/users"})


@router.put("/admin/users/{user_id}/edit")
def edit_user_form(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.user_type != UserTypeEnum.ADMIN:
        raise HTTPException(status_code=403, detail="Доступ запрещён")
    user_obj = db.query(User).filter(User.id == user_id).first()
    if not user_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пользователь не найден")

    workshops = db.query(Workshop).all()
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
def get_profile(current_user: User = Depends(get_current_user)):
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
def edit_profile(
    data: UserBase,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Проверка email, если он передан и отличается
    if data.email and data.email != current_user.email:
        user_with_email = db.query(User).filter(User.email == data.email).first()
        if user_with_email:
            raise HTTPException(status_code=400, detail="Email уже используется другим пользователем")

    # Проверка username, если отличается
    if data.username != current_user.username:
        user_with_username = db.query(User).filter(User.username == data.username).first()
        if user_with_username:
            raise HTTPException(status_code=400, detail="Username уже используется другим пользователем")

    # Обновляем поля
    current_user.name = data.name
    current_user.firstname = data.firstname
    current_user.username = data.username
    current_user.email = data.email  # может быть None
    current_user.telegram = data.telegram  # может быть None

    db.commit()

    return JSONResponse(content={"message": "Профиль обновлён"})



@router.put("/profile/password")
def change_password(
    data: PasswordChangeRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not verify_password(data.current_password, current_user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Текущий пароль введен неверно")
    
    if data.new_password != data.confirm_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Новый пароль и его подтверждение не совпадают")

    current_user.password = get_password_hash(data.new_password)
    db.commit()

    return JSONResponse(content={"message": "Пароль успешно обновлён", "redirect_url": "/profile"})