sqfrom flask import jsonify

from daos.inventory_dao import InventoryDAO
from inventoryservice.db import Session


class Inventory:
    @staticmethod
    def create(body):
        session = Session()
        inventory_item = InventoryDAO(body['product_name'], body['product_price'], body['product_count'])
        session.add(inventory_item)
        session.commit()
        session.refresh(inventory_item)
        session.close()
        return jsonify({'product_id': inventory_item.id}), 200

    @staticmethod
    def get(d_id):
        session = Session()
        # https://docs.sqlalchemy.org/en/14/orm/query.html
        # https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_orm_using_query.htm
        inventory_item = session.query(InventoryDAO).filter(InventoryDAO.id == d_id).first()

        if inventory_item:
            text_out = {
                "product_name:": inventory_item.product_name,
                "product_price": inventory_item.product_price,
                "product_count": inventory_item.product_count,
            }
            session.close()
            return jsonify(text_out), 200
        else:
            session.close()
            return jsonify({'message': f'There is no item in inventory with id {d_id}'}), 404


    @staticmethod
    def get_NonZero(d_id):
        session = Session()
        # https://docs.sqlalchemy.org/en/14/orm/query.html
        # https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_orm_using_query.htm
        inventory_item = session.query(InventoryDAO).filter(InventoryDAO.id == d_id).first()

        if inventory_item:
            text_out = {
                "product_name:": inventory_item.product_name,
                "product_price": inventory_item.product_price,
                "product_count": inventory_item.product_count,
            }
            session.close()
            return jsonify(text_out), 200
        else:
            session.close()
            return jsonify({'message': f'There is no item in inventory with id {d_id}'}), 404


    @staticmethod
    def delete(d_id):
        session = Session()
        effected_rows = session.query(InventoryDAO).filter(InventoryDAO.id == d_id).delete()
        session.commit()
        session.close()
        if effected_rows == 0:
            return jsonify({'message': f'There is no item in inventory with id {d_id}'}), 404
        else:
            return jsonify({'message': 'The item was removed from inventory'}), 200
