from typing import Optional, Union, Dict, Any, List, Type

from sqlalchemy.orm import Session

from core.security import get_password_hash, verify_password
from crud.base import CRUDBase, ModelType
from models.category import Category
from models.item import Item
from models.user import User
from schemas.category import CategoryCreate, CategoryUpdate
from schemas.item import ItemCreate, ItemUpdate
from schemas.user import UserCreate, UserUpdate, SuperUserCreate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            username=obj_in.username,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def create_super_user(self, db: Session, *, obj_in: SuperUserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            username=obj_in.username,
            is_superuser=obj_in.is_superuser,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(self, session: Session, email: str, password: str) -> User:
        user = self.get_by_email(session, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser


class CRUDItem(CRUDBase[Item, ItemCreate, ItemUpdate]):
    def get_multi_for_superuser(db: Session, model: Type[ModelType], skip: int = 0, limit: int = 100) -> List[ModelType]:
        return db.query(model).offset(skip).limit(limit).all()

    def get_multi(db: Session, user, skip: int = 0, limit: int = 100) -> List[ModelType]:
        return db.query(Item).filter(Item.owner_id == user.id).offset(skip).limit(limit).all()


class CRUDCategory(CRUDBase[Category, CategoryCreate, CategoryUpdate]):
    pass


item = CRUDItem(Item)
category = CRUDCategory(Category)
user = CRUDUser(User)
