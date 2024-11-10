import csv
from io import StringIO
from fastapi import Depends, HTTPException, UploadFile
from sqlalchemy.orm import Session
from app.database.database import SessionLocal
from app.repositories.sales import SalesRepo
from app.schemas.sales import SaleCreate


class SalesSvc:
    """Service for processing sales data and interacting with the database."""

    def __init__(self):
        session = SessionLocal()
        self.repo = SalesRepo(session)

    def parse_csv(self, contents: str) -> list[SaleCreate]:
        """Parse CSV contents into a list of SaleCreate objects."""
        csv_data = StringIO(contents)
        reader = csv.DictReader(csv_data)

        sales_data = []
        for row in reader:
            try:
                sale = SaleCreate(
                    transaction_id=row['transaction_id'],
                    transaction_date=row['transaction_date'],
                    customer_id=row.get('customer_id'),
                    channel=row['channel'],
                    product_id=row['product_id'],
                    product_name=row['product_name'],
                    category=row['category'],
                    quantity=int(row['quantity']),
                    unit_price=float(row['unit_price']),
                    discount_amount=float(
                        row['discount_amount']) if row['discount_amount'] else 0.0,
                    total_amount=float(row['total_amount']),
                    payment_method=row['payment_method'],
                    order_status=row['order_status'],
                    shipping_fee=float(
                        row['shipping_fee']) if row['shipping_fee'] else 0.0,
                    tax_amount=float(row['tax_amount']),
                    total_paid=float(row['total_paid']),
                    store_location=row.get('store_location'),
                    salesperson_id=row.get('salesperson_id')
                )
                sales_data.append(sale)
            except KeyError as e:
                raise HTTPException(
                    status_code=400, detail=f"Missing column: {e}")
            except ValueError as e:
                raise HTTPException(
                    status_code=400, detail=f"Invalid data format: {e}")

        return sales_data

    async def process_and_insert_csv(self, file: UploadFile, overwrite: bool) -> int:
        """Check file type, read contents, parse CSV data, and insert into the database."""
        if not file.filename.endswith('.csv'):
            raise HTTPException(
                status_code=400, detail="Invalid file format. Please upload a CSV file.")

        contents = await file.read()
        sales_data = self.parse_csv(contents.decode("utf-8"))

        if overwrite:
            self.repo.clear()

        insert_count = self.repo.insert_sales(sales_data)
        return insert_count
