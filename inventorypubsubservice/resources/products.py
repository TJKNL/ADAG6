import json

from daos.products_dao import ProductsDAO
from db import Session

class Products:

    def create(self, body):
        session = Session()
        product_item = ProductsDAO(body['product_name'], body['product_cost'])

        try:
            session.add(product_item)
            session.commit()
            session.refresh(product_item)
            session.close()
            return json.dumps({'product_id': product_item.id}), 200
        except:

            session.close()
            return "Error: most likely Product already exists in Database", 500


    def delete(self, d_id):
        session = Session()
        effected_rows = session.query(ProductsDAO).filter(ProductsDAO.id == d_id).delete()
        session.commit()
        session.close()
        if effected_rows == 0:
            return json.dumps({'message': f'There is no item in products with id {d_id}'}), 404
        else:
            return json.dumps({'message': 'The item was removed from products'}), 200
