from pydantic import BaseModel

__all__ = ['ItemBase', 'ItemCreate', 'Item']


class ItemBase(BaseModel):
    name: str
    description: str
    price: float
    stock: int
    tag: str


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int

    class Config:
        from_attributes = True
