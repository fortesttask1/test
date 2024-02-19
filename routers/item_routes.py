from typing import Any

from fastapi import APIRouter, HTTPException

import crud.crud
from deps.deps import get_current_user, SessionDep, CurrentUser
from models.item import Item
from schemas.item import ItemCreate, ItemBase, ItemUpdate

router = APIRouter()


@router.get("/items")
def read_items(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve items.
    """
    if current_user.is_superuser:
        return crud.crud.CRUDItem.get_multi_for_superuser(db=session, model=Item, skip=skip, limit=limit)
    else:
        return crud.crud.CRUDItem.get_multi(db=session, user=current_user, skip=skip, limit=limit)


@router.get("/item/{id}")
def read_item(session: SessionDep, current_user: CurrentUser, id: int) -> Any:
    """
    Get item by ID.
    """
    item = crud.crud.item.get(session, id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if not current_user.is_superuser and (item.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    return item


@router.post("/create-item")
def create_item(
    *, session: SessionDep, current_user: CurrentUser, item_in: ItemCreate
) -> Any:
    """
    Create new item.
    """
    item_in.owner_id = current_user.id
    item = crud.crud.item.create(db=session, obj_in=item_in)
    return item


@router.put("/item/{id}", response_model=ItemBase)
def update_item(
    *, session: SessionDep, current_user: CurrentUser, id: int, item_in: ItemUpdate
) -> Any:
    """
    Update an item.
    """
    item = session.get(Item, id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if not current_user.is_superuser and (item.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    # TODO: check this actually works
    update_dict = item_in.dict(exclude_unset=True)
    item.from_orm(update_dict)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@router.delete("/item/{id}")
def delete_item(session: SessionDep, current_user: CurrentUser, id: int):
    """
    Delete an item.
    """
    item = crud.crud.item.remove(session, id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    if not current_user.is_superuser and (item.owner_id != current_user.id):
        raise HTTPException(status_code=400, detail="Not enough permissions")
    session.delete(item)
    session.commit()
    return {"message":"Item deleted successfully"}
