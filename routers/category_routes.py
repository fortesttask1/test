from typing import Any

from fastapi import APIRouter, HTTPException

import crud.crud
from deps.deps import SessionDep, CurrentUser

from schemas.category import CategoryCreate

router = APIRouter()


@router.get("/category/{id}")
def read_category_by_id(session: SessionDep, current_user: CurrentUser, id: int) -> Any:
    """
    Get Category by ID.
    """
    category = crud.crud.category.get(session, id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@router.post("/create-category")
def create_category(
        *, session: SessionDep, current_user: CurrentUser, category_in: CategoryCreate
) -> Any:
    """
    Create new Category.
    """
    if not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    category = crud.crud.category.create(db=session, obj_in=category_in)
    return category


@router.get("/category")
def read_category(
        session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve Category.
    """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Not enough permissions")

    categories = crud.crud.CRUDCategory.get_multi(db=session)
    return categories


@router.delete("/category/{id}")
def delete_category(session: SessionDep, current_user: CurrentUser, id: int):
    """
    Delete a Category.
    """
    category = crud.crud.item.remove(session, id)
    if not category:
        raise HTTPException(status_code=404, detail="Item not found")
    if not current_user.is_superuser:
        raise HTTPException(status_code=400, detail="Not enough permissions")
    session.delete(category)
    session.commit()
    return {"message": "Item deleted successfully"}
