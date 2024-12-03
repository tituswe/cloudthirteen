from typing import List

import numpy as np
import pandas as pd

from app.database.database import SessionLocal
from app.repositories.inventory import InventoryRepo
from app.repositories.sales import SalesRepo
from app.schemas.data import InventoryExpenditureData, ProductReturnsData, SalesByChannelData, SalesByProductData
from app.services.utils import SvcUtils

__all__ = ['SalesAndInventorySvc']


class SalesAndInventorySvc:
    """Service for processing sales and inventory data and interacting with the database."""

    def __init__(self):
        session = SessionLocal()
        self.sales_repo = SalesRepo(session)
        self.inventory_repo = InventoryRepo(session)

    def get_sales_by_product_data(self, start_date: str = None, end_date: str = None) -> List[SalesByProductData]:
        """Retrieve sales by product data."""
        df = self.sales_repo.fetch(start_date, end_date)

        df = (df
              .groupby(['product_name', 'category'])['total_paid']
              .sum()
              .reset_index()
              .rename(columns={'product_name': 'product', 'total_paid': 'revenue'}))

        total_revenue = df['revenue'].sum()

        df['pct_revenue'] = df['revenue'] / total_revenue * 100

        df['revenue'] = df['revenue'].round(2)
        df['pct_revenue'] = df['pct_revenue'].round(1)

        self.close()

        return df.to_dict(orient='records')

    def get_sales_by_channel_data(self, start_date: str = None, end_date: str = None) -> List[SalesByChannelData]:
        """Retrieve sales by channel chart data"""
        df = self.sales_repo.fetch(start_date, end_date)
        df['channel_type'] = np.where(
            df['channel'] == 'Brick & Mortar', 'In Store', 'Online')

        df = (df
              .groupby(['channel', 'channel_type'])['total_paid']
              .sum()
              .reset_index()
              .rename(columns={'total_paid': 'revenue'}))

        total_revenue = df['revenue'].sum()

        df['pct_revenue'] = df['revenue'] / total_revenue * 100

        df['revenue'] = df['revenue'].round(2)
        df['pct_revenue'] = df['pct_revenue'].round(1)

        self.close()

        return df.to_dict(orient='records')

    def get_inventory_expenditure_data(self, start_date: str = None, end_date: str = None, interval: str = None) -> List[InventoryExpenditureData]:
        """Retrieve inventory expenditure chart data"""
        if not interval:
            interval = SvcUtils.get_interval_col(start_date, end_date)

        df = self.inventory_repo.fetch(start_date, end_date)
        df['date'] = pd.to_datetime(df['date'])

        df['interval'] = (df['date']
                          .dt.to_period(interval)
                          .dt.to_timestamp())

        df = (df
              .groupby(['interval', 'product_name', 'cost_price'])[['inventory_level', 'replenishment']]
              .agg({
                  'inventory_level': 'last',
                  'replenishment': 'sum'
              })
              .reset_index()
              .rename(columns={'interval': 'date', 'inventory_level': 'inventory'}))

        df['date'] = df['date'].astype(str)

        df['expenditure'] = df['cost_price'] * df['replenishment']

        df = df.drop(['cost_price'], axis=1)
        df['expenditure'] = df['expenditure'].round(2)

        df = (df
              .pivot(index='date', columns='product_name', values=['inventory', 'replenishment', 'expenditure'])
              .reset_index())
        df.columns = df.columns.map(
            lambda x: f"{x[0]}{':' if x[1] != '' else ''}{x[1]}")

        self.close()

        return df.to_dict(orient='records')

    def get_product_returns_data(self, start_date: str = None, end_date: str = None) -> List[ProductReturnsData]:
        """Retrieve product returns chart data"""
        df = self.sales_repo.fetch(start_date, end_date)
        df['is_refunded'] = np.where(
            df['order_status'] == 'Refunded', 'refunded', 'fulfilled')

        df = (df
              .groupby(['product_name', 'is_refunded'])['quantity']
              .sum()
              .reset_index())

        df = (df
              .pivot(index='product_name', columns='is_refunded', values='quantity')
              .reset_index())

        df['pct_refunded'] = df['refunded'] / \
            (df['fulfilled'] + df['refunded']) * 100

        df['pct_refunded'] = df['pct_refunded'].round(1)

        self.close()

        return df.to_dict(orient='records')

    def close(self):
        self.sales_repo.close()
        self.inventory_repo.close()
