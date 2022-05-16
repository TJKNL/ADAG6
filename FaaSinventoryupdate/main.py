import logging
import os
import time
from message_puller import pull_message, MessagePuller
from pub_sub_util import publish_message
from resources.order import Order

# basic setup
logging.basicConfig(level=logging.INFO)
order = Order()
#project_id = os.environ['project_id']

project_id = "group-6-344214"
subscription_id = "new_order-sub"
"DEZE MOET UITEINDELIJK WERKEN MAAR WERKT NU NIET"
# subscription to new_orders
#MessagePuller(project=project_id, subscription=subscription_id, orders=order)


"DE LOOP HIERONDER WERKT EN KUN JE TESTEN"
while True:
    try:
        pull_message(project_id, subscription_id, order)
        time.sleep(30)
    except Exception as ex:
        logging.info(f"Listening for messages on {subscription_id} threw an exception: {ex}.")
        time.sleep(30)



"DEZE VOOR NU NEGEREN, DIT IS DE TWEEDE DIE UITEINDELIJK MOET WERKEN"
# subscription to fulfilled_orders
#MessagePuller2(project=project_id, subscription="fulfilled_orders-sub", orders=order)



