from pydantic import BaseModel


class ItemBase(BaseModel):
    name: str
    description: str
    category_id: int
    quantity: int
    price: float
    owner_id: int


class ItemCreate(ItemBase):
    pass


class ItemUpdate(ItemBase):
    pass


class Item(ItemBase):
    id: int

    class Config:
        orm_mode = True
