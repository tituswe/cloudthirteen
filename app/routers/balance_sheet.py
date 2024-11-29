from typing import List
from fastapi import APIRouter, Depends, HTTPException

from app.schemas.data import ExpenditureData, RevenueData
from app.services.balance_sheet import BalanceSheetSvc

__all__ = ["router"]


router = APIRouter(prefix="/balance-sheet")


@router.get("/overview",
            description="Get Balance Sheet Overview",
            response_model=None)
def get_overview_data(start_date: str = None,
                      end_date: str = None,
                      interval: str = None,
                      svc: BalanceSheetSvc = Depends()):
    return svc.get_overview_data(start_date, end_date, interval)


@router.get("/revenue",
            description="Calculate Total Revenue",
            response_model=List[RevenueData])
def get_revenue_data(start_date: str = None,
                     end_date: str = None,
                     interval: str = None,
                     svc: BalanceSheetSvc = Depends()):
    return svc.get_revenue_data(start_date, end_date, interval)


@router.get("/expense",
            description="Calculate Total Expenses",
            response_model=List[ExpenditureData])
def get_expense_data(start_date: str = None,
                     end_date: str = None,
                     interval: str = None,
                     svc: BalanceSheetSvc = Depends()):
    return svc.get_expense_data(start_date, end_date, interval)
