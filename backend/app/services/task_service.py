from typing import List, Dict, Any
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, UploadFile
from backend.app.models.bid import Bid, Customer
from backend.app.models.enums import CassetteTypeEnum, KlamerTypeEnum, ManagerEnum, ProfileTypeEnum, StatusEnum, UrgencyEnum
from backend.app.models.files import Files
from backend.app.models.material import Material, Sheets
from backend.app.models.product import Product
from backend.app.models.task import Task, TaskWorkshop
from backend.app.models.user import User
from backend.app.models.workshop import Workshop
from backend.app.schemas.bid import BidCreateResponse
from backend.app.schemas.task import TaskRead
from backend.app.services.user_service import get_user_workshop
from backend.app.database.database_service import AsyncDatabaseService
from backend.app.core.settings import settings
import logging
from backend.app.services import file_service

logger = logging.getLogger(__name__)

async def get_tasks_list(user: User, db: AsyncSession) -> List[TaskRead]:
    """Получает список задач, доступных пользователю."""
    user_workshops = await get_user_workshop(user)

    query = (
        select(Task)
        .join(TaskWorkshop, Task.id == TaskWorkshop.task_id)
        .join(Workshop, Workshop.id == TaskWorkshop.workshop_id)
        .where(Workshop.name.in_(user_workshops))
    )

    result = await db.execute(query)
    tasks = result.scalars().all()

    return [TaskRead.model_validate(task) for task in tasks]


async def get_task_by_id(task_id: int, db: AsyncSession) -> TaskRead:
    """Получает детальную информацию о задаче."""
    db_service = AsyncDatabaseService(db)
    task = await db_service.get_by_id(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return TaskRead.model_validate(task)


async def create_bid_with_tasks(
    bid_info: BidCreateResponse, files: List[UploadFile], db: AsyncSession) -> Dict[str, Any]:
    """
    Создает заявку и связанные с ней задачи.
    """
    db_service = AsyncDatabaseService(db)

    # Проверяем, существует ли заказчик
    customer = await db_service.get_by_id(Customer, bid_info.customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Заказчик не найден")

    # Создаем заявку
    bid_data:Dict[str, Any] = {
        "customer_id": bid_info.customer_id,
        "manager": bid_info.manager,
    }
    bid = await db_service.create(Bid, bid_data)

    # Создаем задачи для заявки
    for task_info in bid_info.tasks:
        # Проверяем, существует ли продукт
        product = await db_service.get_by_field(Product, "type", task_info.product_name)
        if not product:
            raise HTTPException(status_code=404, detail=f"Продукт {task_info.product_name} не найден")

        # Проверяем, существует ли материал
        material = await db_service.get_by_field(Material, "type_id", task_info.material_type)
        if not material:
            raise HTTPException(status_code=404, detail=f"Материал {task_info.material_type} не найден")


    # Сохраняем файлы, если они есть
    if files:
        for file in files:
            await file_service.save_file(bid.id, file, db)

    return {"bid_id": bid.id, "message": "Заявка и задачи успешно созданы"}


async def create_task(
    db: AsyncSession,
    bid_id: int,
    product_id: int,
    material_id: int,
    quantity: int,
    urgency: str,
    status: str,
    waste: str,
    weight: str,
    responsible_user_ids: List[int],
    workshop_ids: List[int],
    file_names: List[str],
    sheet_data: List[Dict[str, Any]],
) -> Task:
    """Создает новую задачу."""
    db_service = AsyncDatabaseService(db)
    # Проверяем существование связанных данных
    bid = await db_service.get_by_id(Bid, bid_id)
    product = await db_service.get_by_id(Product, product_id)
    material = await db_service.get_by_id(Material, material_id)

    if not bid or not product or not material:
        raise HTTPException(
            status_code=400,
            detail="Некоторые из данных (Bid, Product, или Material) не существуют в базе.",
        )

    # Создаем объект задачи
    new_task_data:Dict[str, Any] = {
        "bid_id": bid_id,
        "product_id": product_id,
        "material_id": material_id,
        "quantity": quantity,
        "urgency_id": UrgencyEnum[urgency],
        "status_id": StatusEnum[status],
        "waste": waste,
        "weight": weight,
    }
    new_task = await db_service.create(Task, new_task_data)

    # Добавляем связь с ответственными пользователями
    if responsible_user_ids:
        await db_service.add_relation(
            Task, new_task.id, "responsible_users", User, responsible_user_ids
        )

    # Добавляем связь с мастерскими
    if workshop_ids:
        await db_service.add_relation(
            Task, new_task.id, "workshops", Workshop, workshop_ids
        )

    # Сохраняем файлы для задачи
    for file_name in file_names:
        new_file_data:Dict[str, Any] = {
            "task_id": new_task.id,
            "file_name": file_name,
            "file_path": str(settings.UPLOAD_DIR / str(new_task.id) / file_name),
        }
        await db_service.create(Files, new_file_data)

    # Сохраняем данные для Sheets (при необходимости)
    for sheet in sheet_data:
        new_sheet_data:Dict[str, Any] = {
            "task_id": new_task.id,
            "width_sheet": sheet["width_id"],
            "length_sheet": sheet["length_id"],
            "quantity": sheet["quantity"],
        }
        await db_service.create(Sheets, new_sheet_data)

    return new_task


async def get_products(db: AsyncSession) -> List[Dict[str, Any]]:
    """Получает список продуктов."""
    db_service = AsyncDatabaseService(db)
    products = await db_service.get_all(Product)
    return [{"id": str(item.id), "value": item.type.value} for item in products]


async def get_types(db: AsyncSession) -> tuple[List[str], List[str], List[str], List[str]]:
    """Получает список типов."""
    managers = [managers.value for managers in ManagerEnum]
    profile_values = [profile.name for profile in ProfileTypeEnum]
    klamer_types = [klamer_types.value for klamer_types in KlamerTypeEnum]
    kassete_types = [kassete_types.value for kassete_types in CassetteTypeEnum]
    return managers, profile_values, klamer_types, kassete_types
