from sqlalchemy import Column, String, Integer, Float, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship, backref
from inventoryservice.db import Base
from daos.products_dao import ProductsDAO


class InventoryDAO(Base):
    __tablename__ = 'Inventory'

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('Products.id'), unique=True)
    product_quantity = Column(Integer)
    product_price = Column(Float)
    product = relationship(ProductsDAO.__name__, backref=backref("delivery", uselist=False))

    def __init__(self, product_id, product_quantity, product_price):
        self.product_id = product_id
        self.product_quantity = product_quantity
        self.product_price = product_price
