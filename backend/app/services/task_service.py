import datetime
from typing import List, Dict, Any, Optional, Set
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, UploadFile
from backend.app.models import comment
from backend.app.models.bid import Bid, Customer
from backend.app.models.enums import CassetteTypeEnum, KlamerTypeEnum, ManagerEnum, ProductTypeEnum, ProfileTypeEnum, StatusEnum
from backend.app.models.files import Files, NestFile
from backend.app.models.material import Material, Sheets
from backend.app.models.product import Bracket, Cassette, ExtensionBracket, Klamer, LinearPanel, Product, Profile
from backend.app.models.task import Task, TaskProduct, TaskWorkshop
from backend.app.models.user import User
from backend.app.models.workshop import Workshop
from backend.app.models.comment import Comment
from backend.app.schemas.bid import BidCreate
from backend.app.schemas.comment import CommentRead
from backend.app.schemas.file import UploadedFileResponse
from backend.app.schemas.product_fields import get_product_fields
from backend.app.schemas.task import BidRead, BidRead, CustomerShort, FilesRead, MaterialReadShort, NestFilesRead, ProductTRead, TaskProductRead, TaskRead, TaskWorkshopRead
from backend.app.schemas.user import UserRead
from backend.app.services.file_service import save_file
from backend.app.database.database_service import AsyncDatabaseService
import logging
from sqlalchemy.exc import SQLAlchemyError
from collections import defaultdict
logger = logging.getLogger(__name__)

async def load_user_with_relationships(user_id: int, db: AsyncSession) -> User:
    stmt = (
        select(User)
        .options(
            selectinload(User.workshops),
            selectinload(User.tasks)
        )
        .where(User.id == user_id)
    )
    result = await db.execute(stmt)
    return result.scalar_one()

async def filter_tasks_by_user(tasks: List[Task], current_user: User) -> List[Task]:
    filtered_tasks = []
    user_workshop_ids = {ws.id for ws in current_user.workshops}

    for task in tasks:
        is_responsible = any(user.id == current_user.id for user in task.responsible_users)
        task_workshop_ids = {tw.workshop.id for tw in task.workshops}

        has_common_workshop = not user_workshop_ids.isdisjoint(task_workshop_ids)

        if is_responsible or has_common_workshop:
            filtered_tasks.append(task)

    return filtered_tasks

async def get_bids_with_tasks(current_user: User, db: AsyncSession) -> List[BidRead]:
    current_user = await load_user_with_relationships(current_user.id, db)
    stmt = (
        select(Task)
        .options(
            selectinload(Task.bid).selectinload(Bid.customer),
            selectinload(Task.bid).selectinload(Bid.comments),
            selectinload(Task.task_products)
                .selectinload(TaskProduct.product)
                .selectinload(Product.profile),
            selectinload(Task.task_products)
                .selectinload(TaskProduct.product)
                .selectinload(Product.klamer),
            selectinload(Task.task_products)
                .selectinload(TaskProduct.product)
                .selectinload(Product.bracket),
            selectinload(Task.task_products)
                .selectinload(TaskProduct.product)
                .selectinload(Product.extension_bracket),
            selectinload(Task.task_products)
                .selectinload(TaskProduct.product)
                .selectinload(Product.cassette),
            selectinload(Task.task_products)
                .selectinload(TaskProduct.product)
                .selectinload(Product.linear_panel),
            selectinload(Task.material),
            selectinload(Task.material).selectinload(Material.weights),
            selectinload(Task.sheets),
            selectinload(Task.responsible_users),
            selectinload(Task.workshops).selectinload(TaskWorkshop.workshop),
            selectinload(Task.bid).selectinload(Bid.tasks).selectinload(Task.task_products)
        )
        .order_by(Task.created_at.desc())
    )

    result = await db.execute(stmt)
    tasks = result.scalars().unique().all()

    tasks = await filter_tasks_by_user(tasks, current_user)
    
    bids_dict = defaultdict(list)

    for task in tasks:
        task_products = []
        for tp in task.task_products:
            product_fields = await get_product_fields(tp.product.type)
            task_products.append({
                "product": ProductTRead.model_validate(tp.product, from_attributes=True),
                "color": tp.color,
                "painting": tp.painting,
                "quantity": tp.quantity,
                "done_quantity": tp.done_quantity,
                "product_fields": product_fields,
            })

        task_read = TaskRead(
            id=task.id,
            material=MaterialReadShort.model_validate(task.material, from_attributes=True),
            urgency=task.urgency,
            status=task.status,
            sheets=[
                {
                    "id": s.id,
                    "count": s.quantity,
                    "width": s.width,
                    "length": s.length
                } for s in task.sheets
            ] if task.sheets else [],
            created_at=task.created_at,
            completed_at=task.completed_at,
            workshops=[
                TaskWorkshopRead(
                    workshop_name=tw.workshop.name,
                    status=tw.status,
                    progress_percent=int(tw.progress_percent)
                ) for tw in task.workshops
            ],
            total_quantity=task.total_quantity,
            done_quantity=task.done_quantity,
            progress_percent=int(task.progress_percent),
            task_products=task_products,
        )

        bids_dict[task.bid.id].append((task.bid, task_read))

    bid_reads = []
    for bid_id, task_group in bids_dict.items():
        bid_obj, _ = task_group[0]
        # ⬇ Асинхронный расчет прогресса
        progress = await bid_obj.get_progress_percent(db)
        
        bid_read = BidRead(
            id=bid_obj.id,
            task_number=bid_obj.task_number,
            manager=bid_obj.manager,
            customer=CustomerShort(
                id=bid_obj.customer.id,
                name=bid_obj.customer.name
            ),
            status=bid_obj.status,
            tasks=[t for _, t in task_group],
            progress_percent=int(progress)
        )
        bid_reads.append(bid_read)

    return bid_reads


async def get_bid_by_task_id(task_id: int, db: AsyncSession) -> Optional[BidRead]:
    stmt = (
        select(Task)
        .options(
            selectinload(Task.bid).selectinload(Bid.customer),
            selectinload(Task.bid).selectinload(Bid.comments),
            selectinload(Task.bid).selectinload(Bid.files),
            selectinload(Task.bid).selectinload(Bid.files).selectinload(Files.nest_file),
            selectinload(Task.bid).selectinload(Bid.files).selectinload(Files.nest_file)
            .options(
                selectinload(NestFile.clamp_location),
                selectinload(NestFile.parts),
                selectinload(NestFile.tools),
                ),
            selectinload(Task.bid).selectinload(Bid.comments).selectinload(Comment.user),
            selectinload(Task.material),
            selectinload(Task.material).selectinload(Material.weights),
            selectinload(Task.sheets),
            selectinload(Task.task_products)
            .selectinload(TaskProduct.product)
            .options(
                selectinload(Product.profile),
                selectinload(Product.klamer),
                selectinload(Product.bracket),
                selectinload(Product.extension_bracket),
                selectinload(Product.cassette),
                selectinload(Product.linear_panel),
            ),
            selectinload(Task.workshops).selectinload(TaskWorkshop.workshop),
        )
        .where(Task.id == task_id)
    )

    result = await db.execute(stmt)
    task = result.scalar_one_or_none()

    if task is None:
        return None

    # Перебираем все продукты, прикреплённые к задаче
    task_product_reads = []
    for tp in task.task_products:
        product_fields = await get_product_fields(tp.product.type)

        task_product_reads.append(
            TaskProductRead(
                product=ProductTRead.model_validate(tp.product, from_attributes=True),
                color=tp.color,
                painting=tp.painting,
                quantity=tp.quantity,
                description=tp.description,
                done_quantity=tp.done_quantity,
                product_fields=product_fields
            )
        )

    task_read = TaskRead(
        id=task.id,
        material=MaterialReadShort.model_validate(task.material, from_attributes=True),
        urgency=task.urgency,
        status=task.status,
        created_at=task.created_at,
        completed_at=task.completed_at,
        sheets=[
            {
                "id": s.id,
                "count": s.quantity,
                "width": s.width,
                "length": s.length
            } for s in task.sheets
        ] if task.sheets else [],
        workshops=[
            TaskWorkshopRead(
                workshop_name=tw.workshop.name,
                status=tw.status,
                progress_percent=tw.progress_percent
            ) for tw in task.workshops
        ],
        task_products=task_product_reads,
        total_quantity=task.total_quantity,
        done_quantity=task.done_quantity,
        progress_percent=task.progress_percent
    )
    comments = [
        CommentRead(
            id=comment.id,
            user=UserRead.model_validate(comment.user, from_attributes=True),
            content=comment.content,
            created_at=comment.created_at
        )
        for comment in task.bid.comments
    ]
    files = [
        FilesRead(
            id=file.id,
            filename=file.filename,
            bid_id=file.bid_id,
            file_type=file.file_type,
            file_path=file.file_path
        )
        for file in task.bid.files
    ]
    bid_obj = task.bid
    bid_read = BidRead(
        id=bid_obj.id,
        task_number=bid_obj.task_number,
        manager=bid_obj.manager,
        customer=CustomerShort(
            id=bid_obj.customer.id,
            name=bid_obj.customer.name
        ),
        status=bid_obj.status,
        tasks=[task_read],
        comments=comments,
        files=files,
        nest_files=[
            NestFilesRead.model_validate(file.nest_file, from_attributes=True)
            for file in task.bid.files
            if file.nest_file
        ]
    )

    return bid_read

async def create_bid_with_tasks(user: User, bid_info: BidCreate, files: List[UploadFile], db: AsyncSession):
    try:
        # Сбор всех ID сотрудников
        all_user_ids = {uid for p in bid_info.products for uid in p.employees or []}
        result = await db.execute(select(User).where(User.id.in_(all_user_ids)))
        all_users = {user.id: user for user in result.scalars()}

        # Создание заявки
        new_bid = Bid(
            task_number=bid_info.task_number,
            customer_id=bid_info.customer,
            manager=bid_info.manager,
            status=StatusEnum.NEW,
        )
        db.add(new_bid)
        await db.flush()

        # Комментарий
        if bid_info.comment:
            db.add(Comment(
                bid_id=new_bid.id,
                user_id=user.id,
                content=bid_info.comment,
            ))

        for product_entry in bid_info.products:
            # Создание материала (один на весь продукт)
            material = Material(
                type=product_entry.material.material_type,
                thickness=product_entry.material.material_thickness,
                color=product_entry.material.color
            )
            db.add(material)
            await db.flush()

            # Создание задачи
            task = Task(
                bid_id=new_bid.id,
                material_id=material.id,
                urgency=product_entry.urgency,
                status=StatusEnum.NEW,
            )
            db.add(task)
            await db.flush()

            # Листы
            for sheet in product_entry.sheets:
                db.add(Sheets(
                    task_id=task.id,
                    width=sheet.width,
                    length=sheet.length,
                    quantity=sheet.quantity
                ))

            # Привязка к цехам
            result = await db.execute(select(Workshop).where(Workshop.name.in_(product_entry.workshops)))
            workshops_dict = {w.name.value: w.id for w in result.scalars()}
            for ws_name in product_entry.workshops:
                ws_id = workshops_dict.get(ws_name)
                if ws_id:
                    db.add(TaskWorkshop(task_id=task.id, workshop_id=ws_id, status=StatusEnum.NEW))

            # Привязка ответственных
            await db.refresh(task, attribute_names=["responsible_users"])
            for user_id in product_entry.employees:
                if employee := all_users.get(user_id):
                    task.responsible_users.append(employee)

            # Продукты внутри задачи
            for prod in product_entry.product_details:
                # Создаем продукт
                product = Product(type=product_entry.product_name)
                db.add(product)
                await db.flush()

                if product_entry.product_name == ProductTypeEnum.PROFILE:
                    db.add(Profile(
                        product_id=product.id,
                        profile_type=prod.profile_type,
                        length=prod.length,
                    ))
                elif product_entry.product_name == ProductTypeEnum.KLAMER:
                    db.add(Klamer(
                        product_id=product.id,
                        klamer_type=prod.klamer_type
                    ))
                elif product_entry.product_name == ProductTypeEnum.BRACKET:
                    db.add(Bracket(
                        product_id=product.id,
                        width=prod.width,
                        length=prod.length
                    ))
                elif product_entry.product_name == ProductTypeEnum.EXTENSION_BRACKET:
                    db.add(ExtensionBracket(
                        product_id=product.id,
                        width=prod.width,
                        length=prod.length,
                        heel=prod.has_heel
                    ))
                elif product_entry.product_name == ProductTypeEnum.CASSETTE:
                    db.add(Cassette(
                        product_id=product.id,
                        cassette_type=prod.cassette_type,
                    ))
                elif product_entry.product_name == ProductTypeEnum.LINEAR_PANEL:
                    db.add(LinearPanel(
                        product_id=product.id,
                        field=prod.field,
                        rust=prod.rust,
                        length=prod.length,
                        butt_end=prod.butt_end
                    ))

                # Привязка продукта к задаче с параметрами
                db.add(TaskProduct(
                    task_id=task.id,
                    product_id=product.id,
                    color=prod.color if prod.color else None,
                    painting=bool(prod.painting) if prod.painting is not None else False,
                    quantity=prod.quantity,
                    done_quantity=0,
                    description=prod.description if prod.description else None
                ))

        # Загрузка файлов
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