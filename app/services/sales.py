from typing import List
import pandas as pd

from io import StringIO
from fastapi import HTTPException, UploadFile

from app.database.database import SessionLocal
from app.repositories.sales import SalesRepo
from app.schemas.data import RevenueData
from app.services.utils import SvcUtils


class SalesSvc:
    """Service for processing sales data and interacting with the database."""

    def __init__(self):
        session = SessionLocal()
        self.repo = SalesRepo(session)

    def parse_csv(self, contents: str) -> pd.DataFrame:
        """Parse CSV contents into a Pandas DataFrame."""
        try:
            csv_data = StringIO(contents)
            df = pd.read_csv(csv_data)
            return df
        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f"Error reading CSV: {e}")

    async def process_and_insert_csv(self, file: UploadFile, overwrite: bool) -> int:
        """Read CSV using Pandas and insert data into the database."""
        if not file.filename.endswith('.csv'):
            raise HTTPException(
                status_code=400, detail="Invalid file format. Please upload a CSV file.")

        contents = await file.read()
        df = self.parse_csv(contents.decode("utf-8"))

        if overwrite:
            self.repo.clear()

        insert_count = self.repo.bulk_insert(df)
        return insert_count

    def get_revenue_data(self, start_date: str = None, end_date: str = None, interval: str = None, is_cumulative: bool = True) -> List[RevenueData]:
        """Retrieve total revenue chart data."""
        df = self.repo.fetch(start_date, end_date)
        df['transaction_date'] = pd.to_datetime(df['transaction_date'])

        if not interval:
            interval = SvcUtils.get_interval_col(start_date, end_date)

        df['interval'] = df['transaction_date'].dt.to_period(
            interval).dt.to_timestamp()

        revenue_data = (df
                        .groupby('interval')['total_paid']
                        .sum()
                        .reset_index()
                        .rename(columns={'interval': 'date', 'total_paid': 'revenue'}))

        revenue_data['change'] = revenue_data['revenue'].pct_change() * 100
        revenue_data['change'] = revenue_data['change'].fillna(0)

        if is_cumulative:
            revenue_data['cum_revenue'] = revenue_data['revenue'].cumsum()
            revenue_data['cum_change'] = revenue_data['change'].cumsum()

        revenue_data['date'] = revenue_data['date'].astype(str)

        return revenue_data.to_dict(orient='records')
