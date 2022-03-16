from sqlalchemy import Column, String, Integer, Float

from inventoryservice.db import Base


class InventoryDAO(Base):
    __tablename__ = 'inventory'
    Product_id = Column(Integer, ForeignKey('Products.id'))
    product_count = Column(Integer)


    def __init__(self, product_name, product_price, product_count):
        self.product_name = product_name
        self.product_price = product_price
        self.product_count = product_count
