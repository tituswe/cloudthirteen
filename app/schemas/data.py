from pydantic import BaseModel

__all__ = ["RevenueData", "ExpeditureData"]


class RevenueData(BaseModel):
    date: str
    revenue: float
    change: float
    cum_revenue: float
    cum_change: float


class ExpeditureData(BaseModel):
    date: str
    expense: float
    change: float
    cum_expense: float
    cum_change: float
