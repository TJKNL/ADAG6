import json
import logging
import time
from threading import Thread

from google.cloud import pubsub_v1

from pub_sub_util import publish_message


class Callable:
    def __init__(self, project, inventory):
        self.project = project
        self.inventory = inventory

    def callback(self, message):
        data = json.loads(message.data.decode("utf-8"))
        logging.info(f"Received {data}.")
        results = self.inventory.reduce_inventory(order=data)
        message.ack()


def pull_message(project, subscription, inventory):
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(project, subscription)

    streaming_pull_future = subscriber.subscribe(
        subscription_path, callback=Callable(inventory=inventory, project=project).callback,
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
    def __init__(self, project, subscription, inventory):
        Thread.__init__(self)
        self.project_id = project
        self.subscription_id = subscription
        # self.daemon = True
        self.inventory = inventory
        self.start()

    def run(self):
        while True:
            try:
                pull_message(self.project_id, self.subscription_id, self.inventory)
                time.sleep(30)
            except Exception as ex:
                logging.info(f"Listening for messages on {self.subscription_id} threw an exception: {ex}.")
                time.sleep(30)
