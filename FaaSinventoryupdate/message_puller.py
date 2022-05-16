import json
import logging
import time
from threading import Thread
import pdb

from google.cloud import pubsub_v1

from pub_sub_util import publish_message

def pull_message3(project, subscription, order):
    print("HOEDAN")

def pull_message(project, subscription, order):

    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project, subscription)

    def callback(message):

        logging.info(f"Received {message.data}.")
        # event_type = message.attributes.get("event_type")   # event type as a message attribute
        data = json.loads(message.data.decode("utf-8"))

        logging.info("The new_order is received")
        order.create_order(data)
        unfulfilled_orders = order.get_unfulfilled()
        publish_message(project=project, topic="unfulfilled_orders", message=unfulfilled_orders, event_type="NewOrderAdded")
        message.ack()

    streaming_pull_future = subscriber.subscribe(
        subscription_path, callback=callback, await_callbacks_on_shutdown=True,
    )
    logging.info(f"Listening for messages on {subscription_path}..\n")

    # Wrap subscriber in a 'with' block to automatically call close() when done.
    with subscriber:
        try:
            # When `timeout` is not set, result() will block indefinitely,
            # unless an exception is encountered first.
            streaming_pull_future.result(timeout=60)
        except TimeoutError:
            streaming_pull_future.cancel()

            logging.info("Streaming pull future canceled.")


class MessagePuller(Thread):
    def __init__(self, project, subscription, orders):
        Thread.__init__(self)
        self.project_id = project
        self.subscription_id = subscription
        self.daemon = True
        self.orders = orders
        self.start()

    def run(self):
        for i in range(10)
            try:
                pull_message3(self.project_id, self.subscription_id, self.orders)
                time.sleep(30)
            except Exception as ex:
                logging.info(f"Listening for messages on {self.subscription_id} threw an exception: {ex}.")
                time.sleep(30)


def pull_message2(project, subscription, order):
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project, subscription)

    def callback2(message):

        logging.info(f"Received {message.data}.")
        # event_type = message.attributes.get("event_type")   # event type as a message attribute
        data = json.loads(message.data.decode("utf-8"))

        logging.info("The order status change is received")
        order.update_status(data)
        unfulfilled_orders = order.get_unfulfilled()
        publish_message(project=project, topic="unfulfilled_orders", message=unfulfilled_orders,
                        event_type="OrderStatusUpdated")
        message.ack()

    streaming_pull_future = subscriber.subscribe(
        subscription_path, callback=callback2, await_callbacks_on_shutdown=True,
    )
    logging.info(f"Listening for messages on {subscription_path}..\n")

    # Wrap subscriber in a 'with' block to automatically call close() when done.
    with subscriber:
        try:
            # When `timeout` is not set, result() will block indefinitely,
            # unless an exception is encountered first.
            streaming_pull_future.result(timeout=60)
        except TimeoutError:
            streaming_pull_future.cancel()
            logging.info("Streaming pull future canceled.")


"""class MessagePuller2(Thread):
    def __init__(self, project, subscription, orders):
        Thread.__init__(self)
        self.project_id = project
        self.subscription_id = subscription
        self.daemon = True
        self.orders = orders
        self.start()

    def run(self):

        while True:

            try:
                pull_message2(self.project_id, self.subscription_id, self.orders)
                time.sleep(30)
            except Exception as ex:
                logging.info(f"Listening for messages on {self.subscription_id} threw an exception: {ex}.")
                time.sleep(30)
"""
