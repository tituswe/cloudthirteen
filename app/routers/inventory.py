from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile

from app.services.inventory import InventorySvc

__all__ = ["router"]

router = APIRouter(prefix="/inventory")


@router.post("/upload",
             description="Upload Inventory Data from CSV",
             response_model=None)
async def upload_expenses_csv(file: UploadFile = File(...),
                              overwrite: bool = Query(False),
                              inventory_svc: InventorySvc = Depends()):
    record_count = await inventory_svc.process_and_insert_csv(file, overwrite)

    return {"message": f"Successfully inserted {record_count} records"}
