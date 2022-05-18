from datetime import datetime
from sqlalchemy import desc
from flask import jsonify

from daos.order_dao import OrderDAO
from daos.content_dao import ContentDAO
from db import Session
from resources.content import Content


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
            x = Content.create(body["order_content"], new_id)
            body["order_id"] = new_id

            return body
        else:
            order = OrderDAO(1, datetime.now(), "Unfulfilled")
            session.add(order)
            session.commit()
            session.refresh(order)
            Content.create(body["order_content"], 1)
            session.close()
            body["order_id"] = 1
            return body


    def update_status(body):
        session = Session()
        d_id = body["order_id"]
        order = session.query(OrderDAO).filter(OrderDAO.id == d_id).first()
        order.status = 'Fulfilled'
        session.commit()
        return jsonify({'message': 'The order status was updated'}), 200
