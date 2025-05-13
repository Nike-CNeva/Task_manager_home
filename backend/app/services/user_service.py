from sqlalchemy.orm import Session
from fastapi import HTTPException
from middlewares.auth_middleware import get_password_hash, verify_password
from backend.app.models.models import User, UserTypeEnum, Workshop
from backend.app.database.database_service import DatabaseService
import logging

from backend.app.schemas.schemas import UserSaveForm

logger = logging.getLogger(__name__)

def get_user_by_id(db: Session, user_id: int) -> User:
    """Получает пользователя по ID."""
    db_service = DatabaseService(db)
    user = db_service.get_by_id(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user

def get_user_by_username(db: Session, username: str) -> User:
    """Получает пользователя по логину пользователя или возвращает None."""
    db_service = DatabaseService(db)
    user = db_service.get_by_field(User, "username", username)

    return user

def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
    """Получает список пользователей."""
    db_service = DatabaseService(db)
    return db_service.get_all(User, skip, limit)

def create_user(db: Session, user_data, workshop_ids) -> User:
    """Создает нового пользователя."""
    db_service = DatabaseService(db)

    # Проверка, существует ли пользователь с таким именем
    if get_user_by_username(db, user_data["username"]):
        raise HTTPException(status_code=400, detail="Пользователь с таким именем уже существует")

    # Хешируем пароль
    hashed_password = get_password_hash(user_data["password"])

    # Преобразуем user_type в Enum
    try:
        user_type_enum = UserTypeEnum(user_data["user_type"])
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Некорректный тип пользователя: {user_data['user_type']}")

    # Создаем пользователя
    new_user = db_service.create(User, {
        "name": user_data["name"],
        "username": user_data["username"],
        "password": hashed_password,
        "user_type": user_type_enum,
    })

    # Привязка к цехам
    if workshop_ids:
        workshops = db.query(Workshop).filter(Workshop.id.in_(workshop_ids)).all()
        if len(workshops) != len(workshop_ids):
            raise HTTPException(status_code=400, detail="Один или несколько цехов не найдены")

        db_service.add_relation(User, new_user.id, "workshops", Workshop, workshop_ids)

    return new_user


def update_user(db: Session, form_data: UserSaveForm, workshop_ids: list[int]) -> User:
    """Обновляет данные пользователя."""
    db_service = DatabaseService(db)

    # Получаем пользователя по ID
    user = get_user_by_id(db, form_data.id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    # Преобразуем user_type в Enum (если он передан строкой)
    if isinstance(form_data.user_type, str):
        try:
            user_type_enum = UserTypeEnum(form_data.user_type)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Некорректный тип пользователя: {form_data.user_type}")
    else:
        user_type_enum = form_data.user_type

    # Обновляем данные пользователя
    update_data = {
        "name": form_data.name,
        "firstname": form_data.firstname,
        "username": form_data.username,
        "user_type": user_type_enum,
        "is_active": form_data.is_active
    }
    db_service.update(User, user.id, update_data)

    # Проверяем и обновляем цеха
    if workshop_ids:
        all_workshop_ids = [w.id for w in db_service.get_all(Workshop)]
        if not all(wid in all_workshop_ids for wid in workshop_ids):
            raise HTTPException(status_code=400, detail="Один или несколько цехов не найдены")

        update_user_workshops(db, user.id, workshop_ids)

    return user

def update_user_workshops(db, user_id, new_workshop_ids):
    """Обновляет список цехов пользователя."""
    db_service = DatabaseService(db)
    # Получаем пользователя по ID
    user = get_user_by_id(db, user_id)

    # Получаем текущие объекты Workshop, связанные с пользователем
    current_workshop_ids = {workshop.id for workshop in user.workshops}
    new_workshops = []
    for workshop_id in new_workshop_ids:
        new_workshops.append(workshop_id)

    # Находим цеха, которые нужно добавить
    workshops_to_add = [workshop_id for workshop_id in new_workshops if workshop_id not in current_workshop_ids]

    # Находим цеха, которые нужно удалить
    workshops_to_remove = [workshop_id for workshop_id in current_workshop_ids if workshop_id not in new_workshops]

    # Добавляем новые цеха
    if workshops_to_add:
        db_service.add_relation(User, user_id, "workshops", Workshop, workshops_to_add)

    # Удаляем старые цеха
    if workshops_to_remove:
        db_service.remove_relation(User, user_id, "workshops", Workshop, workshops_to_remove)

def get_user_workshop(user: User) -> set[str]:
    """Определяет список цехов, к которым относится пользователь."""
    return {workshop.name for workshop in user.workshops}
