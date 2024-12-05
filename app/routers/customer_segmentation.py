from typing import List
from fastapi import APIRouter, Depends

from app.schemas.data import CustomerAcquisitionData, CustomersByAgeData, CustomersByChannelData
from app.services.customer_segmentation import CustomerSegmentationSvc

__all__ = ["router"]


router = APIRouter(prefix="/customer-segmentation")


@router.get("/customer-acquisition",
            description="Get Customer Acquisition Data",
            response_model=List[CustomerAcquisitionData])
def get_customer_acquisition_data(start_date: str = None,
                                  end_date: str = None,
                                  interval: str = None,
                                  svc: CustomerSegmentationSvc = Depends()):
    return svc.get_customer_acquisition_data(start_date, end_date, interval)


@router.get("/customers-by-age",
            description="Get Customers by Age Data",
            response_model=List[CustomersByAgeData])
def get_customers_by_age_data(start_date: str = None,
                              end_date: str = None,
                              svc: CustomerSegmentationSvc = Depends()):
    return svc.get_customers_by_age_data(start_date, end_date)


@router.get("/customers-by-channel",
            description="Get Customers by Channel Data",
            response_model=List[CustomersByChannelData])
def get_customers_by_channel_data(start_date: str = None,
                                  end_date: str = None,
                                  svc: CustomerSegmentationSvc = Depends()):
    return svc.get_customers_by_channel_data(start_date, end_date)
