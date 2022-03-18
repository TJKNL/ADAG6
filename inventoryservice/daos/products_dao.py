from sqlalchemy import Column, String, Integer, Float, UniqueConstraint

from inventoryservice.db import Base


class ProductsDAO(Base):
    __tablename__ = 'Products'
    id = Column(Integer, primary_key=True)# Auto generated primary key
    product_name = Column(String, unique=True)
    product_cost = Column(Float)

    def __init__(self, product_name, product_price, product_cost):
        self.product_name = product_name
        self.product_cost = product_cost
