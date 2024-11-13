from io import StringIO
from fastapi import HTTPException, UploadFile
import pandas as pd
from app.database.database import SessionLocal
from app.repositories.expenses import ExpensesRepo
from app.services.utils import SvcUtils

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
        return insert_count

    def get_expense_data(self, start_date: str = None, end_date: str = None, interval: str = None) -> pd.DataFrame:
        """Retrieve expenses data within the optional date range."""
        df = self.repo.fetch(start_date, end_date)
        df['transaction_date'] = pd.to_datetime(df['transaction_date'])

        if not interval:
            interval = SvcUtils.get_interval_col(start_date, end_date)

        df['interval'] = (df['transaction_date']
                          .dt.to_period(interval)
                          .dt.to_timestamp())

        expense_data = (df
                        .groupby('interval')['total_paid']
                        .sum()
                        .reset_index()
                        .rename(columns={'interval': 'date', 'total_paid': 'expense'}))

        expense_data['change'] = (expense_data['expense'].pct_change()
                                  * 100).fillna(0)

        expense_data['cum_expense'] = expense_data['expense'].cumsum()
        expense_data['cum_change'] = (expense_data['cum_expense'].pct_change()
                                      * 100).fillna(0)

        expense_data['date'] = expense_data['date'].astype(str)

        return expense_data.to_dict(orient='records')
