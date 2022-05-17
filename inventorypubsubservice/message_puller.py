import json
import logging
import time
from threading import Thread

from google.cloud import pubsub_v1

from pub_sub_util import publish_message


class Callable:
    def __init__(self, project, order):
        self.project = project
        self.order = order

    def callback(self, message):
        logging.info(f"Received {message.data}.")
        data = json.loads(message.data.decode("utf-8"))

        message.ack()


"""        quantityAva = self.order.get_quantity(data["order_type"])
        if quantityAva < data["quantity"]:
            data = {
                "message": "The requested quantity cannot be satisfied"
            }
            data = json.dumps(data).encode("utf-8")
            publish_message(project=self.project, topic="inventory_status", message=data, event_type="StockUnavailable")
        else:
            data = json.dumps(data).encode("utf-8")
            publish_message(project=self.project, topic="inventory_status", message=data, event_type="StockAvailable")"""


def pull_message(project, subscription, order):
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project, subscription)

    streaming_pull_future = subscriber.subscribe(
        subscription_path, callback=Callable(order=order, project=project).callback,
        await_callbacks_on_shutdown=True,
    )
    logging.info(f"Listening for messages on {subscription_path}..\n")

    # Wrap subscriber in a 'with' block to automatically call close() when done.
    with subscriber:
        try:
            # When `timeout` is not set, result() will block indefinitely,
            # unless an exception is encountered first.
            streaming_pull_future.result(timeout=60)  # see https://docs.python.org/3/library/concurrent.futures.html
        except TimeoutError:
            streaming_pull_future.cancel()
            logging.info("Streaming pull future canceled.")


class MessagePuller(Thread):
    def __init__(self, project, subscription, order):
        Thread.__init__(self)
        self.project_id = project
        self.subscription_id = subscription
        self.daemon = True
        self.order = order
        self.start()

    def run(self):
        while True:
            try:
                pull_message(self.project_id, self.subscription_id, self.order)
                time.sleep(30)
            except Exception as ex:
                logging.info(f"Listening for messages on {self.subscription_id} threw an exception: {ex}.")
                time.sleep(30)
