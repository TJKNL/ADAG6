from flask import jsonify

from daos.inventory_dao import InventoryDAO
from daos.products_dao import ProductsDAO
from db import Session


class Inventory:
    @staticmethod
    def create(body):
        session = Session()
        inventory_item = InventoryDAO(body['product_id'], body['product_quantity'], body['product_price'])

        try:
            session.add(inventory_item)
            session.commit()
            session.refresh(inventory_item)
            session.close()
            return jsonify({'inventory_id': inventory_item.id}), 200
        except:
            session.close()
            return "Error: Most likely inventory item already exists", 500

    @staticmethod
    def get(d_id):
        session = Session()
        # https://docs.sqlalchemy.org/en/14/orm/query.html
        # https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_orm_using_query.htm
        inventory_item = session.query(InventoryDAO).filter(InventoryDAO.product_id == d_id).first()

        if inventory_item:
            product_object = inventory_item.product
            text_out = {
                "product_name": product_object.product_name,
                "product_id": inventory_item.product_id,
                "product_price": inventory_item.product_price,
                "product_cost": product_object.product_cost,
                "product_quantity": inventory_item.product_quantity
            }
            session.close()
            return jsonify(text_out), 200
        else:
            session.close()
            return jsonify({'message': f'There is no item in inventory with id {d_id}'}), 404

    @staticmethod
    def get_nonzero():
        session = Session()
        # https://docs.sqlalchemy.org/en/14/orm/query.html
        # https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_orm_using_query.html
        inventory = session.query(InventoryDAO).filter(InventoryDAO.product_quantity > 0).all()

        if inventory:
            menu = {}
            for p in inventory:
                product_object = p.product  # link to product DB
                text_out = {
                    "product_name": product_object.product_name,
                    "product_price": p.product_price,
                    "product_quantity": p.product_quantity
                }
                menu[p.product_id] = text_out

            session.close()
            return jsonify(menu), 200
        else:
            session.close()
            return jsonify({'message': f'There are no items in inventory'}), 200

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


    @staticmethod
    def reduce_inventory(order):
        session = Session()
        for orders in order["order_content"].items():
            d_id = int(orders[0])
            order_quantity = int(orders[1]["quantity"])
            effected_row = session.query(InventoryDAO).filter(InventoryDAO.product_id == d_id).first()
            old_amount = effected_row.product_quantity
            new_amount = old_amount - order_quantity
            effected_row.product_quantity = new_amount
            session.commit()
            session.close()
        return jsonify({'message': 'The quantity was reduced from inventory'}), 200

    @staticmethod
    def get_all():
        session = Session()
        # https://docs.sqlalchemy.org/en/14/orm/query.html
        # https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_orm_using_query.html
        inventory = session.query(InventoryDAO).all()

        if inventory:
            menu = {}
            for p in inventory:
                product_object = p.product  # link to product DB
                text_out = {
                    "product_name": product_object.product_name,
                    "product_price": p.product_price,
                    "product_quantity": p.product_quantity
                }
                menu[p.product_id] = text_out

            session.close()
            return jsonify(menu), 200
        else:
            session.close()
            return jsonify({'message': f'There are no items in inventory'}), 200
