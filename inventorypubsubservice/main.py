import logging
import os

from message_puller import MessagePuller
from pub_sub_util import create_subscription, create_topic
from resources.inventory import Inventory

logging.basicConfig(level=logging.INFO)

inventory = Inventory()
project_id = os.environ['project_id']

MessagePuller(project=project_id, subscription="new_order-sub", inventory=inventory)
