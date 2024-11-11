from pydantic import BaseModel

__all__ = ["RevenueData"]


class RevenueData(BaseModel):
    date: str
    revenue: float
    change: float
    cum_revenue: float
    cum_change: float
