from sqlalchemy import Column, String, Integer, TIMESTAMP, Float

from db import Base


class ContentDAO(Base):
    __tablename__ = 'content'

    id = Column(Integer, primary_key=True) # Auto generated primary key
    order_id = Column(Integer)
    product_id = Column(Integer)
    product_name = Column(String)
    product_price = Column(Float)
    quantity = Column(Integer)


    def __init__(self, id, order_id, product_id, product_name, product_price, quantity):
        self.id = id
        self.order_id = order_id
        self.product_id = product_id
        self.product_name = product_name
        self.product_price = product_price
        self.quantity = quantity

