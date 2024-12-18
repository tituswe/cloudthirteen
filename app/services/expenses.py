import pandas as pd

from io import StringIO
from fastapi import HTTPException, UploadFile

from app.database.database import SessionLocal
from app.repositories.expenses import ExpensesRepo

__all__ = ['ExpensesSvc']


class ExpensesSvc:
    """Service for processing expenses data and interacting with the database."""

    def __init__(self):
        session = SessionLocal()
        self.repo = ExpensesRepo(session)

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

        self.close()

        return insert_count

    def close(self):
        """Close the database session."""
        self.repo.close()
