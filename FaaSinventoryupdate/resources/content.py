import datetime
from flask import jsonify
from FaaSinventoryupdate.daos.order_dao import OrderDAO
from FaaSinventoryupdate.db import Session


class Content:
    @staticmethod
    def update(d_id, status_text):
        session = Session()
        delivery = session.query(ContentDAO).filter(ContentDAO.id == int(d_id))[0]
        delivery.status.status = status_text
        delivery.status.last_update = datetime.datetime.now()
        session.commit()
        return jsonify({'message': 'The delivery status was updated'}), 200
