from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String

from app.database.database import Base

__all__ = ['InventoryModel']


class InventoryModel(Base):
    __tablename__ = 'inventory'

    date = Column(DateTime, primary_key=True, nullable=False)
    product_name = Column(String, primary_key=True, nullable=False)
    category = Column(String, nullable=False)
    cost_price = Column(Float, nullable=False)
    inventory_level = Column(Integer, nullable=False)
    replenishment = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<InventoryModel(date={self.date}, product_name={self.product_name}, inventory_level={self.inventory_level}, replenishment={self.replenishment})>"
