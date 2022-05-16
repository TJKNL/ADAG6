import logging
import os
import time
from message_puller import pull_message, MessagePuller
from resources.order import Order

# basic setup
logging.basicConfig(level=logging.INFO)
order = Order()
#project_id = os.environ['project_id']

project_id = "group-6-344214"

# subscription to new_orders
MessagePuller(project=project_id, subscription= "new_order-sub", orders=order)

# subscription to fulfilled_orders
MessagePuller(project=project_id, subscription="fulfilled_orders-sub", orders=order)

