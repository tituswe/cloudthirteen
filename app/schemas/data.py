from pydantic import BaseModel

__all__ = ["BalanceSheetData", "RevenueData",
           "ExpenditureData", "SalesByProductData", "SalesByChannelData", "InventoryExpenditureData", "ProductReturnsData"]


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


class ExpenditureData(BaseModel):
    date: str
    expense: float
    change: float
    cum_expense: float
    cum_change: float


class SalesByProductData(BaseModel):
    product: str
    category: str
    revenue: float
    pct_revenue: float


class SalesByChannelData(BaseModel):
    channel: str
    revenue: float
    pct_revenue: float


class InventoryExpenditureData(BaseModel):
    date: str
    product_name: str
    inventory_level: int
    replenishment: int
    expenditure: float


class ProductReturnsData(BaseModel):
    product_name: str
    fulfilled: int
    refunded: int
    pct_refunded: float
