from sqlalchemy import Column, String, Integer, Float, ForeignKey, DateTime, UniqueConstraint

from inventoryservice.db import Base


class InventoryDAO(Base):
    __tablename__ = 'Inventory'

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('Products.id'), unique=True)
    product_quantity = Column(Integer)
    Date_added = Column(DateTime)


    def __init__(self, product_id, product_quantity, Date_added):
        self.product_id = product_id
        self.product_quantity = product_quantity
        self.Date_added = Date_added
