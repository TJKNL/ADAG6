import datetime
from flask import jsonify
from daos.order_dao import OrderDAO
from db import Session
from daos.content_dao import ContentDAO
from sqlalchemy import desc

class Content:
    @staticmethod
    def create(body, order_id):
        session = Session()
        highest_id = session.query(ContentDAO.id).order_by(desc(ContentDAO.id)).first()
        if highest_id:
            new_id = highest_id.id + 1
            for key in body.keys():
                content = ContentDAO(new_id, order_id, key, body[key]["product_name"], body[key]["product_price"], body[key]["quantity"])
                session.add(content)
                session.commit()
                session.refresh(content)
                new_id += 1
        else:
            new_id =  1
            for key in body.keys():
                content = ContentDAO(new_id, order_id, key, body[key]["product_name"], body[key]["product_price"], body[key]["quantity"])
                session.add(content)
                session.commit()
                session.refresh(content)
                new_id += 1

        session.close()
        return jsonify({'message': 'The delivery status was updated'}), 200
