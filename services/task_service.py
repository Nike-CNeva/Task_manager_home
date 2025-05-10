from typing import List, Dict, Any
from sqlalchemy.orm import Session
from fastapi import HTTPException, UploadFile
from models import (
    Bid,
    CassetteTypeEnum,
    Files,
    KlamerTypeEnum,
    ManagerEnum,
    Material,
    Product,
    ProfileTypeEnum,
    Sheets,
    StatusEnum,
    Task,
    TaskWorkshop,
    UrgencyEnum,
    User,
    Workshop,
    Customer
)
from services.user_service import get_user_workshop
from database_service import DatabaseService
from settings import settings
from schemas import BidCreateRequest, TaskCreateRequest
import logging
from services import file_service

logger = logging.getLogger(__name__)


def get_tasks_list(user: User, db: Session) -> List[Task]:
    """Получает список задач, доступных пользователю."""
    db_service = DatabaseService(db)
    user_workshops = get_user_workshop(user)

    tasks_query = (
        db.query(Task)
        .join(TaskWorkshop, Task.id == TaskWorkshop.task_id)  # Явное соединение
        .join(Workshop, Workshop.id == TaskWorkshop.workshop_id)  # Присоединение цехов
        .filter(Workshop.name.in_(user_workshops))  # Фильтр по доступным цехам
    )

    return tasks_query.all()


def get_task_by_id(task_id: int, db: Session) -> Task:
    """Получает детальную информацию о задаче."""
    db_service = DatabaseService(db)
    task = db_service.get_by_id(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return task


async def create_bid_with_tasks(
    bid_info: BidCreateRequest, files: List[UploadFile], db: Session, current_user: User
) -> Dict[str, Any]:
    """
    Создает заявку и связанные с ней задачи.
    """
    db_service = DatabaseService(db)

    # Проверяем, существует ли заказчик
    customer = db_service.get_by_id(Customer, bid_info.customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Заказчик не найден")

    # Создаем заявку
    bid_data = {
        "customer_id": bid_info.customer_id,
        "manager": bid_info.manager,
    }
    bid = db_service.create(Bid, bid_data)

    # Создаем задачи для заявки
    for task_info in bid_info.tasks:
        # Проверяем, существует ли продукт
        product = db_service.get_by_field(Product, "type", task_info.product_name)
        if not product:
            raise HTTPException(status_code=404, detail=f"Продукт {task_info.product_name} не найден")

        # Проверяем, существует ли материал
        material = db_service.get_by_field(Material, "type_id", task_info.material_type)
        if not material:
            raise HTTPException(status_code=404, detail=f"Материал {task_info.material_type} не найден")

        task_data = {
            "bid_id": bid.id,
            "product_id": product.id,
            "material_id": material.id,
            "quantity": task_info.count,
            "urgency_id": UrgencyEnum.MEDIUM,  # Устанавливаем срочность по умолчанию
            "status_id": StatusEnum.NEW,  # Устанавливаем статус по умолчанию
            "waste": task_info.material_color,
            "weight": task_info.material_thickness,
        }
        task = db_service.create(Task, task_data)

    # Сохраняем файлы, если они есть
    if files:
        for file in files:
            await file_service.save_file(task.id, file, "bid_file", db)

    return {"bid_id": bid.id, "message": "Заявка и задачи успешно созданы"}


def create_task(
    db: Session,
    bid_id: int,
    product_id: int,
    material_id: int,
    quantity: int,
    urgency: str,
    status: str,
    waste: str,
    weight: str,
    responsible_user_ids: list,
    workshop_ids: list,
    file_names: list,
    sheet_data: list,
) -> Task:
    """Создает новую задачу."""
    db_service = DatabaseService(db)
    # Проверяем существование связанных данных
    bid = db_service.get_by_id(Bid, bid_id)
    product = db_service.get_by_id(Product, product_id)
    material = db_service.get_by_id(Material, material_id)

    if not bid or not product or not material:
        raise HTTPException(
            status_code=400,
            detail="Некоторые из данных (Bid, Product, или Material) не существуют в базе.",
        )

    # Создаем объект задачи
    new_task_data = {
        "bid_id": bid_id,
        "product_id": product_id,
        "material_id": material_id,
        "quantity": quantity,
        "urgency_id": UrgencyEnum[urgency],
        "status_id": StatusEnum[status],
        "waste": waste,
        "weight": weight,
    }
    new_task = db_service.create(Task, new_task_data)

    # Добавляем связь с ответственными пользователями
    if responsible_user_ids:
        db_service.add_relation(
            Task, new_task.id, "responsible_users", User, responsible_user_ids
        )

    # Добавляем связь с мастерскими
    if workshop_ids:
        db_service.add_relation(
            Task, new_task.id, "workshops", Workshop, workshop_ids
        )

    # Сохраняем файлы для задачи
    for file_name in file_names:
        new_file_data = {
            "task_id": new_task.id,
            "file_name": file_name,
            "file_path": str(settings.UPLOAD_DIR / str(new_task.id) / file_name),
        }
        db_service.create(Files, new_file_data)

    # Сохраняем данные для Sheets (при необходимости)
    for sheet in sheet_data:
        new_sheet_data = {
            "task_id": new_task.id,
            "width_sheet": sheet["width_id"],
            "length_sheet": sheet["length_id"],
            "quantity": sheet["quantity"],
        }
        db_service.create(Sheets, new_sheet_data)

    return new_task


def get_products(db: Session) -> list[dict]:
    """Получает список продуктов."""
    db_service = DatabaseService(db)
    products = db_service.get_all(Product)
    return [{"id": str(item.id), "value": item.type.value} for item in products]


def get_types(db: Session) -> tuple[list[str], list[str], list[str], list[str]]:
    """Получает список типов."""
    managers = [managers.value for managers in ManagerEnum]
    db_service = DatabaseService(db)
    profile_values = [profile.name for profile in ProfileTypeEnum]
    klamer_types = [klamer_types.value for klamer_types in KlamerTypeEnum]
    kassete_types = [kassete_types.value for kassete_types in CassetteTypeEnum]
    return managers, profile_values, klamer_types, kassete_types
