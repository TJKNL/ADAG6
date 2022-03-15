from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship, backref

from daos.status_dao import StatusDAO
from db import Base


class InventoryDAO(Base):
    __tablename__ = 'inventory'
    id = Column(Integer, primary_key=True)  # Auto generated primary key
    product_name = Column(String)
    product_price = Column(Float)
    product_count = Column(Integer)
    # reference to status as foreign key relationship. This will be automatically assigned.
    ## Not neede yet: status_id = Column(Integer, ForeignKey('status.id'))
    # https: // docs.sqlalchemy.org / en / 14 / orm / basic_relationships.html
    # https: // docs.sqlalchemy.org / en / 14 / orm / backref.html
    ##status = relationship(StatusDAO.__name__, backref=backref("delivery", uselist=False))

    def __init__(self, product_name, product_price, product_count):
        self.product_name = product_name
        self.product_price = product_price
        self.product_count = product_count
