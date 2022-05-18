from db import Base, engine
from resources.order import Order
from pub_sub_util import publish_message
import logging
from resources.content import Content
import base64
import json

def update_order_status(event, context):
    pubsub_message = json.loads(base64.b64decode(event['data']).decode('utf-8'))

    try:
        Order.update_status(pubsub_message)
        
    except:
        print("error", ex)
        logging.info(f"Error creating subscription, the exception: {ex}.")


def create_order(event, context):
    pubsub_message = json.loads(base64.b64decode(event["data"]).decode("utf-8"))
    try:
        output = Order.create(pubsub_message)

        results = str.encode(json.dumps(output))
        publish_message(project='group-6-344214', topic="unfulfilled_orders", message=results, event_type="added_to_db")


    except Exception as ex:
        print("error", ex)
        logging.info(f"Error creating subscription, the exception: {ex}.")