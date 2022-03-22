from datetime import datetime
from sqlalchemy import desc
from flask import jsonify

from daos.order_dao import OrderDAO
from daos.content_dao import ContentDAO
from db import Session
from resources.content import Content


class Order:

    # Function to create order.
    @staticmethod
    def create(body):
        session = Session()
        # Create order id: add one to the highest existing order id.
        # At the time of creation, the order status is set to Unfulfilled.
        highest_id = session.query(OrderDAO.id).order_by(desc(OrderDAO.id)).first()

        if highest_id:
            new_id = highest_id.id + 1
            order = OrderDAO(new_id, datetime.now(), "Unfulfilled")
            session.add(order)
            session.commit()
            session.refresh(order)
            session.close()
            Content.create(body["order_content"], new_id)

            return jsonify({'order_id': order.id}), 200

        # If the order table is empty, create order with order id 1.
        else:
            order = OrderDAO(1, datetime.now(), "Unfulfilled")
            session.add(order)
            session.commit()
            session.refresh(order)
            Content.create(body["order_content"], 1)
            session.close()

            return jsonify({'order_id': order.id}), 200

    # Function to get all unfulfilled orders.
    @staticmethod
    def get_unfulfilled():
        session = Session()

        # Extract all orders from order table that have status unfulfilled.
        # Store these order_ids in a list.
        unfulfilled_orders = session.query(OrderDAO).filter(OrderDAO.status == 'Unfulfilled').all()
        unfulfilled_orders_dict = {}

        if unfulfilled_orders:
            order_id_list = []

            for order in unfulfilled_orders:
                order_id_list.append(order.id)

            # For all order_ids, get the order_content from the content table.
            for i in order_id_list:
                unfulfilled_order_content = session.query(ContentDAO).filter(ContentDAO.order_id == i).all()
                order_content = {}

                # For all products in the order content, store the product information.
                for p in unfulfilled_order_content:
                    text_out = {
                        "product_name": p.product_name,
                        "product_price": p.product_price,
                        "product_quantity": p.quantity
                    }
                    order_content[str(p.product_id)] = text_out

                unfulfilled_orders_dict[str(i)] = order_content

            session.close()

            return jsonify(unfulfilled_orders_dict), 200

        else:
            session.close()
            return jsonify({'message': f'There are no unfulfilled orders'}), 404

    # Update the status of an order after order is fulfilled.
    # Input contains order id and new status.
    def update_status(body):
        session = Session()

        d_id = body["d_id"]
        order = session.query(OrderDAO).filter(OrderDAO.id == d_id).first()
        order.status = body["status"]

        session.commit()

        return jsonify({'message': 'The order status was updated'}), 200
