import datetime
from typing import List, Dict, Any
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, UploadFile
from backend.app.models.bid import Bid, Customer
from backend.app.models.enums import CassetteTypeEnum, KlamerTypeEnum, ManagerEnum, ProductTypeEnum, ProfileTypeEnum, StatusEnum
from backend.app.models.files import Files
from backend.app.models.material import Material, Sheets
from backend.app.models.product import Bracket, Cassette, ExtensionBracket, Klamer, LinearPanel, Product, Profile
from backend.app.models.task import Task, TaskWorkshop
from backend.app.models.user import User
from backend.app.models.workshop import Workshop
from backend.app.models.comment import Comment
from backend.app.schemas.bid import BidCreate
from backend.app.schemas.task import TaskRead
from backend.app.schemas.user import UserRead
from backend.app.services.file_service import save_file
from backend.app.services.user_service import get_user_workshop
from backend.app.database.database_service import AsyncDatabaseService
import logging
from sqlalchemy.exc import SQLAlchemyError

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


async def create_bid_with_tasks(user: User, bid_info: BidCreate, files: List[UploadFile], db: AsyncSession):
    try:
        all_user_ids = set()
        for product_data in bid_info.products:
            if product_data.employees:
                all_user_ids.update(product_data.employees)

        # Загружаем из базы всех нужных пользователей одним запросом
        result = await db.execute(select(User).where(User.id.in_(all_user_ids)))
        all_users = {user.id: user for user in result.scalars()}

        # 1. Создаем заявку
        new_bid = Bid(
            task_number=bid_info.task_number,
            customer_id=bid_info.customer,
            manager=bid_info.manager,
        )
        db.add(new_bid)
        await db.flush()  # получаем new_bid.id

        # 2. Комментарии
        if bid_info.comment:
            new_comment = Comment(
                bid_id=new_bid.id,
                user_id=user.id,
                comment=bid_info.comment,
                created_at=datetime.datetime.utcnow(),
            )
            db.add(new_comment)

        for product_data in bid_info.products:
            new_product = Product(
                type=product_data.product_name,
            )
            db.add(new_product)
            await db.flush()

            # 3. Продукты
            if product_data.product_name == ProductTypeEnum.PROFILE.value:
                new_profile = Profile(
                    product_id = new_product.id,
                    profile_type=product_data.product_details["profile_type"],
                    length = product_data.product_details["length"],
                )
                db.add(new_profile)
            elif product_data.product_name == ProductTypeEnum.KLAMER.value:
                new_klamer = Klamer(
                    product_id = new_product.id,
                    klamer_type=product_data.product_details["klamer_type"],
                )
                db.add(new_klamer)
            elif product_data.product_name == ProductTypeEnum.BRACKET.value:
                new_bracket = Bracket(
                    product_id = new_product.id,
                    width = product_data.product_details["width"],
                    length = product_data.product_details["length"],
                )
                db.add(new_bracket)
            elif product_data.product_name == ProductTypeEnum.EXTENSION_BRACKET.value:
                new_extension_bracket = ExtensionBracket(
                    product_id = new_product.id,
                    width = product_data.product_details["width"],
                    length = product_data.product_details["length"],
                    heel = product_data.product_details["heel"],
                )
                db.add(new_extension_bracket)
            elif product_data.product_name == ProductTypeEnum.CASSETTE.value:
                new_kassete = Cassette(
                    product_id = new_product.id,
                    kassete_type=product_data.product_details["kassete_type"],
                    description=product_data.product_details["description"],
                )
                db.add(new_kassete)
            elif product_data.product_name == ProductTypeEnum.LINEAR_PANEL.value:
                new_linear_panel = LinearPanel(
                    product_id = new_product.id,
                    field = product_data.product_details["field"],
                    rust = product_data.product_details["rust"],
                    length = product_data.product_details["length"],
                    butt_end=product_data.product_details["butt_end"],
                )
                db.add(new_linear_panel)

            # 4. Material
            new_material = Material(
                form=product_data.material_form,
                type=product_data.material_type,
                thickness=product_data.material_thickness,
                painting=product_data.painting,
                color=product_data.color,
            )
            db.add(new_material)
            await db.flush()

            # 5. Task
            new_task = Task(
                bid_id=new_bid.id,
                product_id=new_product.id,
                material_id=new_material.id,
                quantity=product_data.product_details["quantity"],
                urgency=product_data.urgency,
                status=StatusEnum("Новая"),
                created_at=datetime.datetime.utcnow(),
            )
            db.add(new_task)
            await db.flush()

            for sheet in product_data.sheets or []:
                new_sheet = Sheets(
                    task_id=new_task.id,
                    width=sheet["width"],
                    length=sheet["length"],
                    quantity=sheet["quantity"],
                )
                db.add(new_sheet)

                workshop_names = product_data.workshops or []  # уже строки

                result = await db.execute(
                    select(Workshop).where(Workshop.name.in_(workshop_names))
                )
                workshops = result.scalars().all()

                # Создаем словарь по строковому имени цеха (т.к. Workshop.name — Enum, но хранится как строка)
                workshops_dict = {w.name.value: w.id for w in workshops}

                for ws_name in workshop_names:
                    ws_id = workshops_dict.get(ws_name)
                    if ws_id:
                        new_task_workshop = TaskWorkshop(
                            task_id=new_task.id,
                            workshop_id=ws_id,
                            status=StatusEnum("Новая"),
                        )
                        db.add(new_task_workshop)
                    else:
                        print(f"Workshop not found for {ws_name}")
            await db.flush()
            # 7. Employees
            await db.refresh(new_task, attribute_names=["responsible_users"])
            for user_id in product_data.employees or []:
                user: User | None = all_users.get(user_id)
                if user:
                    stmt = task_responsible_association.insert().values(task_id=new_task.id, user_id=user.id)
                    await db.execute(stmt)
                    await db.flush()


        # 8. Files
        for file in files:
            await save_file(new_bid.id, file, db)

        await db.commit()
        await db.refresh(new_bid)
        return new_bid

    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка при создании заявки: {str(e)}")

    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Непредвиденная ошибка: {str(e)}")


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

async def create_new_customer_async(db, customer_name: str) -> Customer:
    query = select(Customer).where(Customer.name == customer_name)
    result = await db.execute(query)
    existing_customer = result.scalar_one_or_none()

    if existing_customer:
        return existing_customer
    else:
        new_customer = Customer(name=customer_name)
        db.add(new_customer)
        await db.commit()
        await db.refresh(new_customer)
        return new_customer