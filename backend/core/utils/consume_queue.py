from json import loads
from core.rabbimq.rabbit_manager import (
    RabbitDataConnection,
    RabbitDataConsumer,
    RabbitConsumer,
)


def consume_queue(queue):
    quiz_data = []
    creds = RabbitDataConnection(
        username="guest", password="guest1234", host="localhost"
    )
    consumer_data = RabbitDataConsumer(queue=queue, auto_ack=True)
    consumer = RabbitConsumer(creds=creds, consumer=consumer_data)
    count, message = consumer.consume_messages()
    quiz_data.append(loads(message.decode().replace("'", '"')))
    for x in range(count):
        count, message = consumer.consume_messages()
        quiz_data.append(loads(message.decode().replace("'", '"')))

    return quiz_data
