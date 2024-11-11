import pandas as pd

from fastapi import HTTPException

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.models.sales import SalesModel

__all__ = ['SalesRepo']


class SalesRepo:
    """Repository for handling Sales database operations."""

    def __init__(self, session: Session):
        self.session = session
        self.engine = session.bind

    def get_existing_transaction_ids(self, transaction_ids: list) -> set:
        """Retrieve existing transaction IDs from the database."""
        stmt = select(SalesModel.transaction_id).where(
            SalesModel.transaction_id.in_(transaction_ids))
        result = self.session.execute(stmt)
        return {row[0] for row in result.fetchall()}

    def bulk_insert(self, df: pd.DataFrame) -> int:
        """Insert a DataFrame into the database using Pandas."""
        try:
            required_columns = [
                'transaction_id', 'transaction_date', 'customer_id', 'channel',
                'product_id', 'product_name', 'category', 'quantity', 'unit_price',
                'discount_amount', 'total_amount', 'payment_method', 'order_status',
                'shipping_fee', 'tax_amount', 'total_paid', 'store_location', 'salesperson_id'
            ]
            df = df[required_columns]

            existing_ids = self.get_existing_transaction_ids(
                df['transaction_id'].tolist())

            df = df[~df['transaction_id'].isin(existing_ids)]

            if not df.empty:
                df.to_sql('sales', con=self.engine, if_exists='append',
                          index=False, method='multi', chunksize=10000)

            return len(df)
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error during bulk insert: {str(e)}")

    def fetch(self, start_date: str = None, end_date: str = None) -> pd.DataFrame:
        """Fetch records from the sales table within the optional date range."""
        try:
            query = (self.session.query(SalesModel)
                     .filter(start_date is None or SalesModel.transaction_date >= start_date)
                     .filter(end_date is None or SalesModel.transaction_date <= end_date))

            return pd.read_sql(query.statement, query.session.bind)
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error during fetch: {str(e)}")

    def clear(self):
        """Delete all records from the sales table."""
        try:
            self.session.execute(delete(SalesModel))
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise Exception(f"Database error: {str(e)}")

    def close(self):
        """Close the database session."""
        self.session.close()
