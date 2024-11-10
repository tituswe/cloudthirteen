from pydantic import BaseModel
from typing import Optional
from datetime import datetime

__all__ = ['SaleBase', 'SaleCreate', 'Sale']


class SaleBase(BaseModel):
    transaction_id: str
    transaction_date: datetime
    customer_id: Optional[str] = None
    channel: str
    product_id: str
    product_name: str
    category: str
    quantity: int
    unit_price: float
    discount_amount: Optional[float] = 0.0
    total_amount: float
    payment_method: str
    order_status: str
    shipping_fee: Optional[float] = 0.0
    tax_amount: float
    total_paid: float
    store_location: Optional[str] = None
    salesperson_id: Optional[str] = None


class SaleCreate(SaleBase):
    pass


class Sale(SaleBase):

    class Config:
        from_attributes = True
