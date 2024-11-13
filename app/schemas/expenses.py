from pydantic import BaseModel
from typing import Optional
from datetime import datetime

__all__ = ['ExpenseBase', 'ExpenseCreate', 'Expense']


class ExpenseBase(BaseModel):
    transaction_id: str
    transaction_date: datetime
    expense: str
    total_paid: float
    payment_method: str
    status: str
    is_hq: Optional[bool] = False
    store_location: Optional[str] = None
    employee_id: Optional[str] = None


class ExpenseCreate(ExpenseBase):
    pass


class Expense(ExpenseBase):
    class Config:
        from_attributes = True
