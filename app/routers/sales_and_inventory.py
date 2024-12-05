from typing import List
from fastapi import APIRouter, Depends

from app.schemas.data import ProductReturnsData, SalesByChannelData, SalesByProductData
from app.services.sales_and_inventory import SalesAndInventorySvc

__all__ = ["router"]


router = APIRouter(prefix="/sales-and-inventory")


@router.get("/sales-by-product",
            description="Get Sales Data by Product",
            response_model=List[SalesByProductData])
def get_sales_by_product_data(start_date: str = None,
                              end_date: str = None,
                              svc: SalesAndInventorySvc = Depends()):
    return svc.get_sales_by_product_data(start_date, end_date)


@router.get("/sales-by-channel",
            description="Get Sales Data by Channel",
            response_model=List[SalesByChannelData])
def get_sales_by_channel_data(start_date: str = None,
                              end_date: str = None,
                              svc: SalesAndInventorySvc = Depends()):
    return svc.get_sales_by_channel_data(start_date, end_date)


@router.get("/inventory-expense",
            description="Get Inventory Expense Data")
def get_inventory_expenditure_data(start_date: str = None,
                                   end_date: str = None,
                                   interval: str = None,
                                   svc: SalesAndInventorySvc = Depends()):
    return svc.get_inventory_expenditure_data(
        start_date, end_date, interval)


@router.get("/product-returns",
            description="Get Product Returns Data",
            response_model=List[ProductReturnsData])
def get_product_returns_data(start_date: str = None,
                             end_date: str = None,
                             svc: SalesAndInventorySvc = Depends()):
    return svc.get_product_returns_data(start_date, end_date)
