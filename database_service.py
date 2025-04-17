from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from fastapi import HTTPException
from typing import List, TypeVar, Type, Optional
from models import Base

T = TypeVar('T', bound=Base) # type: ignore


class DatabaseService:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self, model: Type[T], skip: int = 0, limit: int = 100) -> List[T]:
        """Получает все записи из таблицы."""
        try:
            return self.db.query(model).offset(skip).limit(limit).all()
        except SQLAlchemyError as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    def get_by_id(self, model: Type[T], id: int) -> Optional[T]:
        """Получает запись по ID."""
        try:
            return self.db.query(model).filter(model.id == id).first()
        except SQLAlchemyError as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    def get_by_field(self, model: Type[T], field_name: str, field_value: str) -> Optional[T]:
        """Получает запись по значению поля."""
        try:
            field = getattr(model, field_name)
            return self.db.query(model).filter(field == field_value).first()
        except SQLAlchemyError as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    def create(self, model: Type[T], data: dict) -> T:
        """Создает новую запись."""
        try:
            db_item = model(**data)
            self.db.add(db_item)
            self.db.commit()
            self.db.refresh(db_item)
            return db_item
        except IntegrityError as e:
            self.db.rollback()
            raise HTTPException(status_code=400, detail=f"Integrity error: {str(e)}")
        except SQLAlchemyError as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    def update(self, model: Type[T], id: int, data: dict) -> Optional[T]:
        """Обновляет запись по ID."""
        try:
            db_item = self.get_by_id(model, id)
            if db_item:
                for key, value in data.items():
                    setattr(db_item, key, value)
                self.db.commit()
                self.db.refresh(db_item)
            return db_item
        except SQLAlchemyError as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    def delete(self, model: Type[T], id: int) -> bool:
        """Удаляет запись по ID."""
        try:
            db_item = self.get_by_id(model, id)
            if db_item:
                self.db.delete(db_item)
                self.db.commit()
                return True
            return False
        except SQLAlchemyError as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    def add_relation(self, parent_model: Type[T], parent_id: int, relation_name: str, child_model: Type[T], child_ids: List[int]):
        """Добавляет связь между родительской и дочерними моделями."""
        try:
            parent_item = self.get_by_id(parent_model, parent_id)
            if not parent_item:
                raise ValueError(f"Parent item with id {parent_id} not found")

            relation = getattr(parent_item, relation_name)
            child_items = self.db.query(child_model).filter(child_model.id.in_(child_ids)).all()
            relation.extend(child_items)
            self.db.commit()
        except SQLAlchemyError as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    def remove_relation(self, parent_model: Type[T], parent_id: int, relation_name: str, child_model: Type[T], child_ids: List[int]):
        """Удаляет связь между родительской и дочерними моделями."""
        try:
            parent_item = self.get_by_id(parent_model, parent_id)
            if not parent_item:
                raise ValueError(f"Parent item with id {parent_id} not found")

            relation = getattr(parent_item, relation_name)
            child_items = self.db.query(child_model).filter(child_model.id.in_(child_ids)).all()
            for child in child_items:
                if child in relation:
                    relation.remove(child)
            self.db.commit()
        except SQLAlchemyError as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
