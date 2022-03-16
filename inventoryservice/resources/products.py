from flask import jsonify

from daos.products_dao import ProductsDAO
from inventoryservice.db import Session

class Products:
    @staticmethod
    def create(body):
        session = Session()
        product_item = ProductsDAO(body['product_name'], body['product_price'],body['product_cost'])
        session.add(product_item)
        session.commit()
        session.refresh(product_item)
        session.close()
        return jsonify({'product_id': product_item.id}), 200
