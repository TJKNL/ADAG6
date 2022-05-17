from flask import jsonify

from daos.products_dao import ProductsDAO
from db import Session


class Products:
    @staticmethod
    def get():
        session = Session()
        products = session.query(ProductsDAO)

        if products:
            text_out = {
                "product_name": products.product_name,
                "product_id:": products.product_id,
                "product_cost": products.product_cost,
            }
            session.close()
            return jsonify(text_out), 200
        else:
            session.close()
            return jsonify({'message': "There are no products in db"}), 404
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

    @staticmethod
    def delete(d_id):
        session = Session()
        effected_rows = session.query(ProductsDAO).filter(ProductsDAO.id == d_id).delete()
        session.commit()
        session.close()
        if effected_rows == 0:
            return jsonify({'message': f'There is no item in products with id {d_id}'}), 404
        else:
            return jsonify({'message': 'The item was removed from products'}), 200
