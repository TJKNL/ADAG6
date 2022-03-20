from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref

from daos.status_dao import ContentDAO
from db import Base


class OrderDAO(Base):
    __tablename__ = 'delivery'
    id = Column(Integer, primary_key=True)  # Auto generated primary key
    order_time = Column(DateTime)
    status = Column(String)
    # reference to status as foreign key relationship. This will be automatically assigned.
    content_id = Column(Integer, ForeignKey('status.id'))
    # https: // docs.sqlalchemy.org / en / 14 / orm / basic_relationships.html
    # https: // docs.sqlalchemy.org / en / 14 / orm / backref.html
    content = relationship(ContentDAO.__name__, backref=backref("delivery", uselist=False))

    def __init__(self, id, order_time, status, content):
        self.id = id
        self.order_time = order_time
        self.status = status
        self.content = content
