import pandas as pd

from fastapi import HTTPException
from sqlalchemy import delete, select

from app.models.expenses import ExpensesModel
from app.repositories.base import BaseRepo

__all__ = ['ExpensesRepo']


class ExpensesRepo(BaseRepo):
    """Repository for handling Expenses database operations."""

    def get_existing_transaction_ids(self, transaction_ids: list) -> set:
        """Retrieve existing transaction IDs from the database."""
        stmt = select(ExpensesModel.transaction_id).where(
            ExpensesModel.transaction_id.in_(transaction_ids))
        result = self.session.execute(stmt)
        return {row[0] for row in result.fetchall()}

    def bulk_insert(self, df: pd.DataFrame) -> int:
        """Insert a DataFrame into the database using Pandas."""
        try:
            required_columns = [
                'transaction_id', 'transaction_date', 'expense', 'total_paid', 'payment_method', 'status', 'is_hq', 'store_location', 'employee_id'
            ]
            df = df[required_columns]

            existing_ids = self.get_existing_transaction_ids(
                df['transaction_id'].tolist())

            df = df[~df['transaction_id'].isin(existing_ids)]

            if not df.empty:
                df.to_sql('expenses', con=self.engine, if_exists='append',
                          index=False, method='multi', chunksize=10000)

            return len(df)
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error during bulk insert: {str(e)}")

    def fetch(self, start_date: str = None, end_date: str = None) -> pd.DataFrame:
        """Fetch records from the expenses table within the optional date range."""
        try:
            query = (self.session.query(ExpensesModel)
                     .filter(start_date is None or ExpensesModel.transaction_date >= start_date)
                     .filter(end_date is None or ExpensesModel.transaction_date <= end_date))

            return pd.read_sql(query.statement, query.session.bind)
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error during fetch: {str(e)}")

    def clear(self):
        """Delete all records from the expenses table."""
        try:
            stmt = select(ExpensesModel)
            self.session.execute(delete(stmt))
            self.session.commit()
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error during clear: {str(e)}")
