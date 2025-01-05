from typing import List
from datetime import datetime

import numpy as np
import pandas as pd

from app.database.database import SessionLocal
from app.repositories.expenses import ExpensesRepo
from app.repositories.sales import SalesRepo
from app.schemas.data import DashboardData
from app.services.utils import SvcUtils

__all__ = ['DashboardSvc']


class DashboardSvc:
    """Service for processing dashboard data and interacting with the database."""

    def __init__(self):
        session = SessionLocal()
        self.sales_repo = SalesRepo(session)
        self.expenses_repo = ExpensesRepo(session)

    def get_dashboard_data(self, start_date: str = None, end_date: str = None, interval: str = None) -> DashboardData:
        if not interval:
            interval = SvcUtils.get_interval_col(start_date, end_date)

        revenue_df = self.sales_repo.fetch(start_date, end_date)
        expenses_df = self.expenses_repo.fetch(start_date, end_date)

        revenue = revenue_df['total_paid'].sum().round(2)
        expenses = expenses_df['total_paid'].sum().round(2)
        pnl = revenue - expenses
        sales = revenue_df.shape[0]
        customers = 5283  # Placeholder value

        revenue_pct_change = 12.1
        pnl_pct_change = 5.4
        sales_pct_change = 3.2
        customers_pct_change = 2.3

        self.close()

        return {
            "revenue": revenue,
            "revenue_change": revenue_pct_change,
            "pnl": pnl,
            "pnl_change": pnl_pct_change,
            "sales": sales,
            "sales_change": sales_pct_change,
            "customers": customers,
            "customers_change": customers_pct_change,
        }

    def close(self):
        self.sales_repo.close()
        self.expenses_repo.close()
