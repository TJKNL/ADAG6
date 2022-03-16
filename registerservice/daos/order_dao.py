from sqlalchemy import Column, String, Integer, Float

from inventoryservice.db import Base


class OrderDAO(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer)
    product_id = Column(Integer, ForeignKey('Products.id'))
    product_name = Column(String, ForeignKey('Products.Name'))
    count = Column(Integer)
    total_value = Column(Integer)



    def __init__(self, product_name, product_price, product_count, prices_list):
        self.product_name = product_name
        #self.product_price = product_price niet nodig?
        self.product_count = product_count
        self.count = product_count
        self.total_value_products = product_count * product_price




