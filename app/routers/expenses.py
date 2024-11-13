from typing import List
from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile

from app.schemas.data import ExpeditureData, RevenueData
from app.services.expenses import ExpensesSvc

__all__ = ["router"]

router = APIRouter(prefix="/expenses")


@router.post("/upload",
             description="Upload Expenses Data from CSV",
             response_model=None)
async def upload_expenses_csv(file: UploadFile = File(...),
                              overwrite: bool = Query(False),
                              expenses_svc: ExpensesSvc = Depends()):
    try:
        record_count = await expenses_svc.process_and_insert_csv(file, overwrite)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        expenses_svc.repo.close()

    return {"message": f"Successfully inserted {record_count} records"}


@router.get("/expense",
            description="Calculate Total Expenses",
            response_model=List[ExpeditureData])
def get_expense_data(start_date: str = None,
                     end_date: str = None,
                     interval: str = None,
                     expenses_svc: ExpensesSvc = Depends()):
    try:
        expense_data = expenses_svc.get_expense_data(
            start_date, end_date, interval)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        expenses_svc.repo.close()

    return expense_data
