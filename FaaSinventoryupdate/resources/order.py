from datetime import datetime
from sqlalchemy import desc
from flask import jsonify

from FaaSinventoryupdate.daos.order_dao import OrderDAO
from FaaSinventoryupdate.daos.content_dao import ContentDAO
from FaaSinventoryupdate.db import Session
from FaaSinventoryupdate.resources.content import Content


class Order:
    @staticmethod
    def create(body):
        session = Session()
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
        else:
            order = OrderDAO(1, datetime.now(), "Unfulfilled")
            session.add(order)
            session.commit()
            session.refresh(order)
            Content.create(body["order_content"], 1)
            session.close()
            return jsonify({'order_id': order.id}), 200

    @staticmethod
    def get_unfulfilled():
        session = Session()

        unfulfilled_orders = session.query(OrderDAO).filter(OrderDAO.status == 'Unfulfilled').all()
        unfulfilled_orders_dict = {}

        if unfulfilled_orders:
            order_id_list = []

            for order in unfulfilled_orders:
                order_id_list.append(order.id)

            for i in order_id_list:
                unfulfilled_order_content = session.query(ContentDAO).filter(ContentDAO.order_id == i).all()
                order_content = {}

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
