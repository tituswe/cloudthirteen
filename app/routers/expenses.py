from typing import List
from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile

from app.services.expenses import ExpensesSvc

__all__ = ["router"]

router = APIRouter(prefix="/expenses")


@router.post("/upload",
             description="Upload Expenses Data from CSV",
             response_model=None)
async def upload_expenses_csv(file: UploadFile = File(...),
                              overwrite: bool = Query(False),
                              expenses_svc: ExpensesSvc = Depends()):
    record_count = await expenses_svc.process_and_insert_csv(file, overwrite)

    return {"message": f"Successfully inserted {record_count} records"}
