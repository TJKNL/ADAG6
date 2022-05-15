import logging
import os

from message_puller import MessagePuller, MessagePuller2
from pub_sub_util import publish_message
from resources.order import Order

# basic setup
logging.basicConfig(level=logging.INFO)
order = Order()
project_id = os.environ['project_id']

# subscription to new_orders
MessagePuller(project=project_id, subscription="new_order-sub", orders=order)

# subscription to fulfilled_orders
MessagePuller2(project=project_id, subscription="fulfilled_orders_sub", orders=order)



