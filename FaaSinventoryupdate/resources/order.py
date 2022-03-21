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
        # https://docs.sqlalchemy.org/en/14/orm/query.html
        # https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_orm_using_query.htm
        unfulfilled_orders = session.query(OrderDAO).filter(OrderDao.status == 'Unfulfilled').all()

        if unfulfilled_orders:
            unfulfilled_orders_list = {"unfulfilled_orders_list": []}
            order_id_list = []

            for order in unfulfilled_orders:
                text_out = {
                    "id:": order.id,
                }
                order_id_list.append(text_out)

            for i in order_id_list:
                unfulfilled_order_content = session.query(ContentDAO).filter(ContentDAO.id == i.id).all()

                order_content = {"order_content": []}

                for p in unfulfilled_order_content:
                    text_out = {
                        "product_id:": p.product_id,
                        "product_name": p.product_name,
                        "product_price": p.product_price,
                        "product_quantity": p.product_quantity
                    }
                    order_content["order_content"].append(text_out)

                unfulfilled_orders_list["unfulfilled_orders_list"].append(order_content)

            session.close()

            return jsonify(unfulfilled_orders_list), 200

        else:
            session.close()
            return jsonify({'message': f'There are no unfulfilled orders'}), 404

    #
    # @staticmethod
    # def delete(d_id):
    #     session = Session()
    #     effected_rows = session.query(DeliveryDAO).filter(DeliveryDAO.id == int(d_id)).delete()
    #     session.commit()
    #     session.close()
    #     if effected_rows == 0:
    #         return jsonify({'message': f'There is no delivery with id {d_id}'}), 404
    #     else:
    #         return jsonify({'message': 'The delivery was removed'}), 200
