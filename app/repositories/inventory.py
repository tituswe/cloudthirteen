import pandas as pd

from fastapi import HTTPException
from sqlalchemy import delete, select

from app.models.inventory import InventoryModel
from app.repositories.base import BaseRepo


__all__ = ['InventoryRepo']


class InventoryRepo(BaseRepo):
    """Repository for handling Inventory database operations."""

    def bulk_insert(self, df: pd.DataFrame) -> int:
        """Insert a DataFrame into the database using Pandas."""
        try:
            required_columns = [
                'date', 'product_name', 'category', 'cost_price', 'inventory_level', 'replenishment'
            ]
            df = df[required_columns]

            if not df.empty:
                df.to_sql('inventory', con=self.engine, if_exists='append',
                          index=False, method='multi', chunksize=10000)

            return len(df)
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error during bulk insert: {str(e)}")

    def fetch(self, start_date: str = None, end_date: str = None) -> pd.DataFrame:
        """Fetch records from the inventory table within the optional date range."""
        try:
            query = (self.session.query(InventoryModel)
                     .filter(start_date is None or InventoryModel.date >= start_date)
                     .filter(end_date is None or InventoryModel.date <= end_date))

            return pd.read_sql(query.statement, query.session.bind)
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error during fetch: {str(e)}")

    def clear(self):
        """Delete all records from the expenses table."""
        try:
            stmt = select(InventoryModel)
            self.session.execute(delete(stmt))
            self.session.commit()
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error during clear: {str(e)}")
