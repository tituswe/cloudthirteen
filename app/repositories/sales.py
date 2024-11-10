from fastapi import HTTPException
from sqlalchemy import delete
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert

from app.models.sales import SalesModel
from app.schemas.sales import SaleCreate


class SalesRepo:
    """Repository for handling Sales database operations."""

    def __init__(self, session: Session):
        self.session = session

    def insert_sales(self, sales_data: list[SaleCreate]):
        """Insert a list of sales records into the database, ignoring duplicates."""
        try:
            inserted_count = 0
            for sale in sales_data:
                stmt = (
                    insert(SalesModel)
                    .values(**sale.model_dump())
                    .on_conflict_do_nothing(index_elements=['transaction_id'])
                    .returning(SalesModel.transaction_id)
                )
                result = self.session.execute(stmt)

                inserted_count += len(result.fetchall())

            self.session.commit()
            return inserted_count
        except Exception as e:
            self.session.rollback()
            raise Exception(f"Database error: {str(e)}")

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
