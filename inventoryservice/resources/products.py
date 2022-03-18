from flask import jsonify

from daos.products_dao import ProductsDAO
from inventoryservice.db import Session

class Products:
    @staticmethod
    def create(body):
        session = Session()
        product_item = ProductsDAO(body['product_name'], body['product_cost'])

        try:
            session.add(product_item)
            session.commit()
            session.refresh(product_item)
            session.close()
            return jsonify({'product_id': product_item.id}), 200
        except:

            session.close()
            return "Error: most likely Product already exists in Database", 500
