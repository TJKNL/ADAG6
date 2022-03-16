from sqlalchemy import Column, String, Integer, Float, ForeignKey

from inventoryservice.db import Base


class InventoryDAO(Base):
    __tablename__ = 'Inventory'

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('Products.id'))
    product_count = Column(Integer)


    def __init__(self, product_id, product_count):
        self.product_id = product_id
        self.product_count = product_count
