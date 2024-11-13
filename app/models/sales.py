from decimal import Decimal
from sqlalchemy import Column, DateTime, Float, Integer, String

from app.database.database import Base

__all__ = ["SalesModel"]


class SalesModel(Base):
    __tablename__ = 'sales'

    transaction_id = Column(String, primary_key=True)
    transaction_date = Column(DateTime, nullable=False)
    customer_id = Column(String, nullable=True)
    channel = Column(String, nullable=False)
    product_id = Column(String, nullable=False)
    product_name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    discount_amount = Column(Float, nullable=True, default=0.0)
    total_amount = Column(Float, nullable=False)
    payment_method = Column(String, nullable=False)
    order_status = Column(String, nullable=False)
    shipping_fee = Column(Float, nullable=True, default=0.0)
    tax_amount = Column(Float, nullable=False)
    total_paid = Column(Float, nullable=False)
    store_location = Column(String, nullable=True)
    salesperson_id = Column(String, nullable=True)

    def __repr__(self):
        return f"<SalesModel(transaction_id='{self.transaction_id}', category-{self.category}, total_paid={self.total_paid})>"
