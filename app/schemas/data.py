from pydantic import BaseModel

__all__ = ["BalanceSheetData", "RevenueData",
           "ExpenditureData", "CustomerAcquisitionData", "CustomersByAgeData", "CustomersByChannelData", "SalesByProductData", "SalesByChannelData", "InventoryExpenditureData", "ProductReturnsData"]


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


class CustomerAcquisitionData(BaseModel):
    date: str
    customers: int
    cum_customers: int


class CustomersByAgeData(BaseModel):
    age: str
    age_label: str
    customers: int
    pct_customers: float


class CustomersByChannelData(BaseModel):
    channel: str
    customers: int
    pct_customers: float


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
    # arbitrary number of inventory items


class ProductReturnsData(BaseModel):
    product_name: str
    fulfilled: int
    refunded: int
    pct_refunded: float
