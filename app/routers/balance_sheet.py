from typing import List
from fastapi import APIRouter, Depends, HTTPException

from app.schemas.data import ExpeditureData, RevenueData
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
    try:
        overview_data = svc.get_overview_data(
            start_date, end_date, interval)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        svc.close()

    return overview_data


@router.get("/revenue",
            description="Calculate Total Revenue",
            response_model=List[RevenueData])
def get_revenue_data(start_date: str = None,
                     end_date: str = None,
                     interval: str = None,
                     svc: BalanceSheetSvc = Depends()):
    try:
        revenue_data = svc.get_revenue_data(
            start_date, end_date, interval)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        svc.close()

    return revenue_data


@router.get("/expense",
            description="Calculate Total Expenses",
            response_model=List[ExpeditureData])
def get_expense_data(start_date: str = None,
                     end_date: str = None,
                     interval: str = None,
                     svc: BalanceSheetSvc = Depends()):
    try:
        expense_data = svc.get_expense_data(
            start_date, end_date, interval)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        svc.close()

    return expense_data
