from sqlalchemy import String, Integer, Float, Column
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String)
    price = Column(Float)
    quantity = Column(Integer)