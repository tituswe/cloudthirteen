from typing import List
from datetime import datetime

import numpy as np
import pandas as pd

from app.schemas.data import CustomerAcquisitionData, CustomersByAgeData, CustomersByChannelData
from app.services.utils import SvcUtils

__all__ = ['CustomerSegmentationSvc']


class CustomerSegmentationSvc:
    """Service for processing customer segmentation data and interacting with the database."""

    def __init__(self):
        pass

    def get_customer_acquisition_data(self, start_date: str = None, end_date: str = None, interval: str = None) -> List[CustomerAcquisitionData]:
        """Retrieve customer acquisition chart data"""
        if not start_date:
            start_date = (datetime.now() - pd.DateOffset(years=1)
                          ).strftime('%Y-%m-%d')

        if not end_date:
            end_date = datetime.now().strftime('%Y-%m-%d')

        if not interval:
            interval = SvcUtils.get_interval_col(start_date, end_date)

        dates = pd.date_range(start=start_date, end=end_date)
        a, b = 2, 5
        beta_random = np.random.beta(a, b, size=len(dates))
        customers = (beta_random * 200).astype(int)

        df = pd.DataFrame({
            "date": dates,
            "customers": customers
        })

        df['interval'] = (df['date']
                          .dt.to_period(interval)
                          .dt.to_timestamp())

        df = (df
              .groupby(['interval'])['customers']
              .sum()
              .reset_index()
              .rename(columns={'interval': 'date'}))

        df['cum_customers'] = df['customers'].cumsum()

        df['date'] = df['date'].astype(str)

        return df.to_dict('records')

    def get_customers_by_age_data(self, start_date: str = None, end_date: str = None) -> List[CustomersByAgeData]:
        """Retrieve customers by age chart data"""
        if not start_date:
            start_date = (datetime.now() - pd.DateOffset(years=1)
                          ).strftime('%Y-%m-%d')

        if not end_date:
            end_date = datetime.now().strftime('%Y-%m-%d')

        age_map = {
            '0': 'Gen A',
            '12': 'Gen Z',
            '28': 'Millenials',
            '44': 'Gen X',
            '60': 'Baby Boomers'
        }
        num_days = (datetime.strptime(end_date, '%Y-%m-%d')
                    - datetime.strptime(start_date, '%Y-%m-%d')).days
        a, b = 2, 5
        beta_random = np.random.beta(a, b, size=len(age_map))
        customers = (beta_random * num_days * 100).astype(int)
        total_customers = customers.sum()
        pct_customers = customers / total_customers * 100

        df = pd.DataFrame({
            "age": age_map.keys(),
            "age_label": age_map.values(),
            "customers": customers,
            "pct_customers": pct_customers
        })

        df['pct_customers'] = df['pct_customers'].round(1)

        return df.to_dict('records')

    def get_customers_by_channel_data(self, start_date: str = None, end_date: str = None) -> List[CustomersByChannelData]:
        """Retrieve customers by channel chart data"""
        if not start_date:
            start_date = (datetime.now() - pd.DateOffset(years=1)
                          ).strftime('%Y-%m-%d')

        if not end_date:
            end_date = datetime.now().strftime('%Y-%m-%d')

        channels = ['Amazon', 'Brick & Mortar', 'Lazada', 'Shopee', 'Website']
        num_days = (datetime.strptime(end_date, '%Y-%m-%d')
                    - datetime.strptime(start_date, '%Y-%m-%d')).days
        a, b = 5, 2
        beta_random = np.random.beta(a, b, size=len(channels))
        customers = (beta_random * num_days * 120).astype(int)
        total_customers = customers.sum()
        pct_customers = customers / total_customers * 100

        df = pd.DataFrame({
            "channel": channels,
            "customers": customers,
            "pct_customers": pct_customers
        })

        df['pct_customers'] = df['pct_customers'].round(1)

        return df.to_dict('records')

    def close(self):
        pass
