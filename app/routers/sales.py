from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile

from app.services.sales import SalesSvc

__all__ = ["router"]

router = APIRouter()


@router.post("/sales/upload", description="Upload Sales Data from CSV", response_model=None)
async def upload_sales_csv(file: UploadFile = File(...), overwrite: bool = Query(False), sales_svc: SalesSvc = Depends()):
    try:
        record_count = await sales_svc.process_and_insert_csv(file, overwrite)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        sales_svc.repo.close()

    return {"message": f"Successfully inserted {record_count} records"}
