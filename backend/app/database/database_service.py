from enum import Enum
from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm.attributes import InstrumentedAttribute
from fastapi import HTTPException
from typing import Any, List, Sequence, TypeVar, Type, Optional
from typing import Protocol, runtime_checkable

@runtime_checkable
class HasID(Protocol):
    id: Any  # Mapped[int] — заменяем на Any, чтобы избежать проблем в Protocol

T = TypeVar('T', bound=HasID)

class AsyncDatabaseService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(
        self,
        model: Type[T],
        skip: int = 0,
        limit: int = 100,
        options: Optional[List[Any]] = None
    ) -> Sequence[T]:
        try:
            stmt: Select = select(model).offset(skip).limit(limit)
            if options:
                for opt in options:
                    stmt = stmt.options(opt)
            result = await self.db.execute(stmt)
            return result.scalars().all()
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    async def get_by_id(self, model: Type[T], id: int) -> Optional[T]:
        try:
            result = await self.db.execute(select(model).where(model.id == id))
            return result.scalars().first()
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    async def get_by_field(self, model: Type[T], field_name: str, field_value: Any) -> Optional[T]:
        try:
            field: InstrumentedAttribute[Any] = getattr(model, field_name)
            result = await self.db.execute(select(model).where(field == field_value))
            return result.scalars().first()
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    async def create(self, model: Type[T], data: dict[str, Any]) -> T:
        try:
            db_item = model(**data)
            self.db.add(db_item)
            await self.db.commit()
            await self.db.refresh(db_item)
            return db_item
        except IntegrityError as e:
            await self.db.rollback()
            raise HTTPException(status_code=400, detail=f"Integrity error: {str(e)}")
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    async def update(self, model: Type[T], id: int, data: dict[str, Any]) -> Optional[T]:
        try:
            db_item = await self.get_by_id(model, id)
            if db_item:
                for key, value in data.items():
                    setattr(db_item, key, value)
                await self.db.commit()
                await self.db.refresh(db_item)
            return db_item
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    async def delete(self, model: Type[T], id: int) -> bool:
        try:
            db_item = await self.get_by_id(model, id)
            if db_item:
                self.db.delete(db_item)
                await self.db.commit()
                return True
            return False
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    async def add_relation(self, parent_model: Type[T], parent_id: int, relation_name: str, child_model: Type[T], child_ids: List[int]) -> None:
        try:
            parent_item = await self.get_by_id(parent_model, parent_id)
            if not parent_item:
                raise ValueError(f"Parent item with id {parent_id} not found")

            relation = getattr(parent_item, relation_name)
            result = await self.db.execute(select(child_model).where(child_model.id.in_(child_ids)))
            child_items = result.scalars().all()
            relation.extend(child_items)
            await self.db.commit()
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    async def remove_relation(self, parent_model: Type[T], parent_id: int, relation_name: str, child_model: Type[T], child_ids: List[int]) -> None:
        try:
            parent_item = await self.get_by_id(parent_model, parent_id)
            if not parent_item:
                raise ValueError(f"Parent item with id {parent_id} not found")

            relation = getattr(parent_item, relation_name)
            result = await self.db.execute(select(child_model).where(child_model.id.in_(child_ids)))
            child_items = result.scalars().all()
            for child in child_items:
                if child in relation:
                    relation.remove(child)
            await self.db.commit()
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    async def ensure_enum_seeded(
        self,
        model: Type[T],
        enum_cls: Type[Enum],
        enum_field: str = "name"
    ) -> None:
        try:
            # Получаем существующие значения поля (например, name)
            existing = await self.db.execute(select(getattr(model, enum_field)))
            existing_values = {row[0] for row in existing.all()}

            # Добавляем недостающие
            new_items = []
            for enum_item in enum_cls:
                if enum_item not in existing_values:
                    item_data = {enum_field: enum_item}
                    new_items.append(model(**item_data))

            if new_items:
                self.db.add_all(new_items)
                await self.db.commit()
                print(f"[✓] Добавлены новые значения: {[item.name for item in new_items]}")
            else:
                print("[✓] Все значения из Enum уже присутствуют в таблице.")
        except SQLAlchemyError as e:
            await self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Enum seed error: {str(e)}")