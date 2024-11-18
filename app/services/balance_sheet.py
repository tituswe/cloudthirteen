from typing import List

import pandas as pd

from app.database.database import SessionLocal
from app.repositories.expenses import ExpensesRepo
from app.repositories.sales import SalesRepo
from app.schemas.data import BalanceSheetData, RevenueData
from app.services.utils import SvcUtils

__all__ = ['BalanceSheetSvc']


class BalanceSheetSvc:
    """Service for processing balance sheet data and interacting with the database."""

    def __init__(self):
        session = SessionLocal()
        self.sales_repo = SalesRepo(session)
        self.expenses_repo = ExpensesRepo(session)

    def get_overview_data(self, start_date: str = None, end_date: str = None, interval: str = None) -> List[BalanceSheetData]:
        """Retrieve balance sheet overview data."""
        if not interval:
            interval = SvcUtils.get_interval_col(start_date, end_date)

        revenue_df = self.sales_repo.fetch(start_date, end_date)
        revenue_df['transaction_date'] = (pd.
                                          to_datetime(revenue_df['transaction_date']))
        revenue_df['interval'] = (revenue_df['transaction_date']
                                  .dt.to_period(interval)
                                  .dt.to_timestamp())
        revenue_df = (revenue_df
                      .groupby('interval')['total_paid']
                      .sum()
                      .reset_index()
                      .rename(columns={'interval': 'date', 'total_paid': 'revenue'}))

        expenses_df = self.expenses_repo.fetch(start_date, end_date)
        expenses_df['transaction_date'] = (pd
                                           .to_datetime(expenses_df['transaction_date']))
        expenses_df['interval'] = (expenses_df['transaction_date']
                                   .dt.to_period(interval)
                                   .dt.to_timestamp())
        expenses_df = (expenses_df
                       .groupby('interval')['total_paid']
                       .sum()
                       .reset_index()
                       .rename(columns={'interval': 'date', 'total_paid': 'expense'}))

        overview_df = (revenue_df
                       .merge(expenses_df, on='date', how='outer')
                       .fillna(0)
                       .sort_values('date')
                       .reset_index(drop=True))
        overview_df['margin'] = ((overview_df['revenue']
                                  - overview_df['expense']))
        overview_df['cum_margin'] = overview_df['margin'].cumsum()
        overview_df['date'] = overview_df['date'].astype(str)

        return overview_df.to_dict(orient='records')

    def get_revenue_data(self, start_date: str = None, end_date: str = None, interval: str = None) -> List[RevenueData]:
        """Retrieve total revenue chart data."""
        if not interval:
            interval = SvcUtils.get_interval_col(start_date, end_date)

        df = self.sales_repo.fetch(start_date, end_date)
        df['transaction_date'] = pd.to_datetime(df['transaction_date'])

        df['interval'] = (df['transaction_date']
                          .dt.to_period(interval)
                          .dt.to_timestamp())

        df = (df
              .groupby('interval')['total_paid']
              .sum()
              .reset_index()
              .rename(columns={'interval': 'date', 'total_paid': 'revenue'}))

        df['change'] = (df['revenue'].pct_change()
                        * 100).fillna(0)

        df['cum_revenue'] = df['revenue'].cumsum()
        df['cum_change'] = (df['cum_revenue'].pct_change()
                            * 100).fillna(0)

        df['date'] = df['date'].astype(str)

        return df.to_dict(orient='records')

    def get_expense_data(self, start_date: str = None, end_date: str = None, interval: str = None) -> pd.DataFrame:
        """Retrieve expenses data within the optional date range."""
        if not interval:
            interval = SvcUtils.get_interval_col(start_date, end_date)

        df = self.expenses_repo.fetch(start_date, end_date)
        df['transaction_date'] = pd.to_datetime(df['transaction_date'])

        df['interval'] = (df['transaction_date']
                          .dt.to_period(interval)
                          .dt.to_timestamp())

        df = (df
              .groupby('interval')['total_paid']
              .sum()
              .reset_index()
              .rename(columns={'interval': 'date', 'total_paid': 'expense'}))

        df['change'] = (df['expense'].pct_change()
                        * 100).fillna(0)

        df['cum_expense'] = df['expense'].cumsum()
        df['cum_change'] = (df['cum_expense'].pct_change()
                            * 100).fillna(0)

        df['date'] = df['date'].astype(str)

        return df.to_dict(orient='records')

    def close(self):
        self.sales_repo.close()
        self.expenses_repo.close()
