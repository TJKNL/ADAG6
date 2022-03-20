from datetime import datetime
from sqlalchemy import desc
from flask import jsonify

from FaaSinventoryupdate.daos.order_dao import OrderDAO
from FaaSinventoryupdate.daos.content_dao import ContentDAO
from FaaSinventoryupdate.db import Session


class Order:
    @staticmethod
    def create(body):
        session = Session()
        highest_id = session.query(OrderDAO.id).order_by(desc(OrderDAO.id)).first()

        if highest_id:
            new_id = highest_id.id + 1
            contentlist = {}
            for content in body["order_content"]:
                contentlist.append(ContentDAO(new_id, content['product_id'], content["product_name"],content["product_price"], content['quantity']))

            order = OrderDAO(new_id, datetime.now(), "Unfulfilled", contentlist)
            session.add(order)
            session.commit()
            session.refresh(order)
            session.close()
            return jsonify({'order_id': order.id}), 200
        else:
            order = OrderDAO(1, datetime.now(), "test", ContentDAO(1, 1, "test", 12.1, 1))
            session.add(order)
            session.commit()
            session.refresh(order)
            session.close()
            return jsonify({'order_id': order.id}), 200

    @staticmethod
    def get(d_id):
        session = Session()
        # https://docs.sqlalchemy.org/en/14/orm/query.html
        # https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_orm_using_query.htm
        delivery = session.query(DeliveryDAO).filter(DeliveryDAO.id == int(d_id)).first()

        if delivery:
            status_obj = delivery.status
            text_out = {
                "customer_id:": delivery.customer_id,
                "provider_id": delivery.provider_id,
                "package_id": delivery.package_id,
                "order_time": delivery.order_time.isoformat(),
                "delivery_time": delivery.delivery_time.isoformat(),
                "status": {
                    "status": status_obj.status,
                    "last_update": status_obj.last_update.isoformat(),
                }
            }
            session.close()
            return jsonify(text_out), 200
        else:
            session.close()
            return jsonify({'message': f'There is no delivery with id {d_id}'}), 404

    @staticmethod
    def delete(d_id):
        session = Session()
        effected_rows = session.query(DeliveryDAO).filter(DeliveryDAO.id == int(d_id)).delete()
        session.commit()
        session.close()
        if effected_rows == 0:
            return jsonify({'message': f'There is no delivery with id {d_id}'}), 404
        else:
            return jsonify({'message': 'The delivery was removed'}), 200
