from sqlalchemy import Column, Float, Integer, String

from app.database.database import Base

__all__ = ["ItemModel"]


class ItemModel(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    price = Column(Float)
    stock = Column(Integer)
    tag = Column(String)
