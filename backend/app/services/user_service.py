from typing import Any, Dict, List, Optional, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from backend.app.middlewares.auth_middleware import get_password_hash
from backend.app.models.enums import UserTypeEnum
from backend.app.models.user import User
from backend.app.models.workshop import Workshop
from backend.app.schemas.user import UserSaveForm

from backend.app.database.database_service import AsyncDatabaseService
import logging


logger = logging.getLogger(__name__)

async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
    """Получает пользователя по ID."""
    db_service = AsyncDatabaseService(db)
    user = await db_service.get_by_id(User, user_id)  # нужно ожидать асинхронный запрос
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user

async def get_user_by_username(db: AsyncSession, username: str) -> Optional[User]:
    """Получает пользователя по логину пользователя или возвращает None."""
    db_service = AsyncDatabaseService(db)
    user = await db_service.get_by_field(User, "username", username)  # нужно ожидать асинхронный запрос
    return user 

async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100) -> Sequence[User]:
    """Получает список пользователей."""
    db_service = AsyncDatabaseService(db)
    return await db_service.get_all(User, skip, limit)  # нужно ожидать асинхронный запрос

async def create_user(db: AsyncSession, user_data: UserSaveForm, workshop_ids: List[int]) -> User:
    """Создает нового пользователя."""
    db_service = AsyncDatabaseService(db)

    # Проверка, существует ли пользователь с таким именем
    user = await get_user_by_username(db, user_data.username)  # нужно ожидать асинхронный запрос
    if user:
        raise HTTPException(status_code=400, detail="Пользователь с таким именем уже существует")

    # Хешируем пароль
    hashed_password = get_password_hash(user_data.password)

    # Преобразуем user_type в Enum
    try:
        user_type_enum = UserTypeEnum(user_data.user_type)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Некорректный тип пользователя: {user_data.user_type}")

    # Создаем пользователя
    new_user = await db_service.create(User, {
        "name": user_data.name,
        "username": user_data.username,
        "password": hashed_password,
        "user_type": user_type_enum,
    })

    # Привязка к цехам
    if workshop_ids:
        workshops = await db.execute(Workshop.__table__.select().filter(Workshop.id.in_(workshop_ids)))  # асинхронный запрос
        workshops = workshops.scalars().all()
        if len(workshops) != len(workshop_ids):
            raise HTTPException(status_code=400, detail="Один или несколько цехов не найдены")

        await db_service.add_relation(User, new_user.id, "workshops", Workshop, workshop_ids)

    return new_user


async def update_user(db: AsyncSession, form_data: UserSaveForm, workshop_ids: list[int]) -> User:
    """Обновляет данные пользователя."""
    db_service = AsyncDatabaseService(db)

    # Получаем пользователя по ID
    user = await get_user_by_id(db, form_data.id)  # нужно ожидать асинхронный запрос
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")


    user_type_enum = form_data.user_type

    # Обновляем данные пользователя
    update_data: Dict[str, Any] = {
        "name": form_data.name,
        "firstname": form_data.firstname,
        "username": form_data.username,
        "user_type": user_type_enum,
        "is_active": form_data.is_active
    }
    await db_service.update(User, user.id, update_data)  # нужно ожидать асинхронный запрос

    # Проверяем и обновляем цеха
    if workshop_ids:
        all_workshop_ids = [w.id for w in await db_service.get_all(Workshop)]  # асинхронный запрос
        if not all(wid in all_workshop_ids for wid in workshop_ids):
            raise HTTPException(status_code=400, detail="Один или несколько цехов не найдены")

        await update_user_workshops(db, user.id, workshop_ids)

    return user

async def update_user_workshops(db: AsyncSession, user_id: int, new_workshop_ids: List[int]):
    """Обновляет список цехов пользователя."""
    db_service = AsyncDatabaseService(db)
    # Получаем пользователя по ID
    user = await get_user_by_id(db, user_id)  # нужно ожидать асинхронный запрос
    if user is None:
        raise ValueError(f"Пользователь с ID {user_id} не найден")
    
    # Получаем текущие объекты Workshop, связанные с пользователем
    current_workshop_ids = {workshop.id for workshop in user.workshops}
    new_workshops: List[int] = []
    for workshop_id in new_workshop_ids:
        new_workshops.append(workshop_id)

    # Находим цеха, которые нужно добавить
    workshops_to_add = [workshop_id for workshop_id in new_workshops if workshop_id not in current_workshop_ids]

    # Находим цеха, которые нужно удалить
    workshops_to_remove = [workshop_id for workshop_id in current_workshop_ids if workshop_id not in new_workshops]

    # Добавляем новые цеха
    if workshops_to_add:
        await db_service.add_relation(User, user_id, "workshops", Workshop, workshops_to_add)  # асинхронный запрос

    # Удаляем старые цеха
    if workshops_to_remove:
        await db_service.remove_relation(User, user_id, "workshops", Workshop, workshops_to_remove)  # асинхронный запрос

async def get_user_workshop(user: User) -> set[str]:
    """Определяет список цехов, к которым относится пользователь."""
    return {workshop.name for workshop in user.workshops}
