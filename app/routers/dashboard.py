from fastapi import APIRouter, Depends

from app.schemas.data import DashboardData
from app.services.customer_segmentation import CustomerSegmentationSvc
from app.services.dashboard import DashboardSvc

__all__ = ["router"]


router = APIRouter(prefix="/dashboard")


@router.get("/",
            description="Get Dashboard Data",
            response_model=DashboardData)
def get_customer_acquisition_data(start_date: str = None,
                                  end_date: str = None,
                                  interval: str = None,
                                  svc: DashboardSvc = Depends()):
    return svc.get_dashboard_data(start_date, end_date, interval)
