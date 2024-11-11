from typing import List
from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile

from app.schemas.data import RevenueData
from app.services.sales import SalesSvc

__all__ = ["router"]

router = APIRouter(prefix="/sales")


@router.post("/upload", description="Upload Sales Data from CSV", response_model=None)
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


@router.get("/revenue", description="Calculate Total Revenue", response_model=List[RevenueData])
def get_revenue_data(start_date: str = None, end_date: str = None, interval: str = None, is_cumulative: bool = True, sales_svc: SalesSvc = Depends()):
    try:
        revenue_data = sales_svc.get_revenue_data(
            start_date, end_date, interval, is_cumulative)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        sales_svc.repo.close()

    return revenue_data
