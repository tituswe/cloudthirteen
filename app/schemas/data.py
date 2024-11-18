from pydantic import BaseModel

__all__ = ["BalanceSheetData", "RevenueData", "ExpeditureData"]


class BalanceSheetData(BaseModel):
    date: str
    revenue: float
    expense: float
    margin: float
    cum_margin: float


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
