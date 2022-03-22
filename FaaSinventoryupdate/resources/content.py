from flask import jsonify
from db import Session
from daos.content_dao import ContentDAO
from sqlalchemy import desc


class Content:

    # Function to add content to order.
    @staticmethod
    def create(body, order_id):
        session = Session()

        # Create order content id: add one to the highest existing order content id.
        highest_id = session.query(ContentDAO.id).order_by(desc(ContentDAO.id)).first()

        if highest_id:
            new_id = highest_id.id + 1

            # For every product in the order, add product id and product information to table.
            for key in body.keys():
                content = ContentDAO(new_id, order_id, key, body[key]["product_name"], body[key]["product_price"],
                                     body[key]["quantity"])
                session.add(content)
                session.commit()
                session.refresh(content)
                new_id += 1

        # If there are no orders yet, order content id is set to 1.
        else:
            new_id = 1

            # For every product in the order, add product id and product information to table.
            for key in body.keys():
                content = ContentDAO(new_id, order_id, key, body[key]["product_name"], body[key]["product_price"],
                                     body[key]["quantity"])
                session.add(content)
                session.commit()
                session.refresh(content)
                new_id += 1

        session.close()

        return jsonify({'message': 'The delivery status was updated'}), 200
