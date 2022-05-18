import logging
from google.cloud import pubsub_v1

def publish_message(project, topic, message, event_type):
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project, topic)
    future = publisher.publish(topic_path, message, event_type=event_type)
    try:
        future.result()
    except Exception as ex:
        logging.info(ex)
        future.cancel()
    logging.info(f"Published event {event_type} to {topic_path}.")