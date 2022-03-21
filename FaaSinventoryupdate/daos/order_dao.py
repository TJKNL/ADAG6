from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref

from FaaSinventoryupdate.daos.content_dao import ContentDAO
from FaaSinventoryupdate.db import Base


class OrderDAO(Base):
    __tablename__ = 'order_table'
    id = Column(Integer, primary_key=True)  # Auto generated primary key
    order_time = Column(DateTime)
    status = Column(String)
    # reference to status as foreign key relationship. This will be automatically assigned.
    content_id = Column(Integer, ForeignKey('content.id'))

    def __init__(self, id, order_time, status, content_id):
        self.id = id
        self.order_time = order_time
        self.status = status
        self.content = content_id
