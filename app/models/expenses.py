from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String

from app.database.database import Base

__all__ = ["SalesModel"]


class ExpensesModel(Base):
    __tablename__ = 'expenses'

    transaction_id = Column(String, primary_key=True)
    transaction_date = Column(DateTime, nullable=False)
    expense = Column(String, nullable=False)
    total_paid = Column(Float, nullable=False)
    payment_method = Column(String, nullable=False)
    status = Column(String, nullable=False)
    is_hq = Column(Boolean, default=False)
    store_location = Column(String)
    employee_id = Column(String)

    def __repr__(self):
        return f"<ExpensesModel(transaction_id={self.transaction_id}, expense={self.expense}, total_paid={self.total_paid})>"
