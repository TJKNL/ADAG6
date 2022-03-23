from sqlalchemy import Column, String, Integer, DateTime, ForeignKey

from db import Base

# Create OrderDAO with order id, order creation time and order status
class OrderDAO(Base):
    __tablename__ = 'order_table'
    id = Column(Integer, primary_key=True)
    order_time = Column(DateTime)
    status = Column(String)

    def __init__(self, id, order_time, status):
        self.id = id
        self.order_time = order_time
        self.status = status

