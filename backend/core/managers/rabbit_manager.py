import logging
from dataclasses import dataclass
from enum import Enum
import colorlog
import pika

handler = logging.StreamHandler()
handler.setFormatter(
    colorlog.ColoredFormatter(
        "\033[35m| \033[0m\033[32mRabbitMQ-\033[0m%(log_color)s%(levelname)-8s%(reset)s %(blue)s%(message)s",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "red,bg_white",
        },
    )
)

logger = colorlog.getLogger()
logger.addHandler(handler)
logger.setLevel(logging.INFO)


class Exchange(Enum):
    DEFAULT = ""
    DIRECT = "direct"
    TOPIC = "topic"
    FANOUT = "fanout"


@dataclass
class RabbitDataConnection:
    username: str
    password: str
    host: str = "localhost"


@dataclass
class RabbitDataProducer:
    exchange: str
    routing_key: str
    body: str


@dataclass
class RabbitDataExchange:
    exchange: str
    exchange_type: Exchange
    durable: bool = True


@dataclass
class RabbitDataQueue:
    queue: str
    durable: bool = True


@dataclass
class RabbitDataConsumer:
    queue: str
    auto_ack: bool


class RabbitConnection:
    def __init__(
        self,
        creds: RabbitDataConnection,
    ):
        assert isinstance(creds, RabbitDataConnection)
        self.creds = creds

    def _get_connection(self):
        credentials = pika.PlainCredentials(self.creds.username, self.creds.password)
        parameters = pika.ConnectionParameters(
            host=self.creds.host, credentials=credentials
        )
        connection = pika.BlockingConnection(parameters)
        logger.info(f"Connecting to {self.creds.host} as {self.creds.username}")
        return connection.channel()

    def check_is_channel_and_connection_open(self):
        with self._get_connection() as channel:
            return channel.is_open, channel.connection.is_open


class RabbitProducer(RabbitConnection):
    def __init__(
        self,
        creds: RabbitDataConnection,
        producer: RabbitDataProducer,
    ):
        assert isinstance(producer, RabbitDataProducer)
        super().__init__(creds)
        self.producer = producer

    def send(self):
        with self._get_connection() as channel:
            channel.basic_publish(
                exchange=self.producer.exchange,
                routing_key=self.producer.routing_key,
                body=self.producer.body,
                properties=pika.BasicProperties(
                    delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
                ),
            )
            logger.info(f"Sent {self.producer.body} as {self.producer.exchange}")


class RabbitExchange(RabbitConnection):
    def __init__(
        self,
        creds: RabbitDataConnection,
        exchange: RabbitDataExchange,
    ):
        assert isinstance(exchange, RabbitDataExchange)
        super().__init__(creds)
        self.exchange = exchange

    def create_exchange(self):
        with self._get_connection() as channel:
            channel.exchange_declare(
                exchange=self.exchange.exchange,
                exchange_type=self.exchange.exchange_type,
                durable=self.exchange.durable,
            )
            logger.info(
                f"Exchange {self.exchange.exchange} - {self.exchange.exchange_type} has been created"
            )


class RabbitQueue(RabbitConnection):
    def __init__(self, creds: RabbitDataConnection, queue: RabbitDataQueue):
        assert isinstance(queue, RabbitDataQueue)
        super().__init__(creds)
        self.queue = queue

    def create_queue(self):
        with self._get_connection() as channel:
            channel.queue_declare(
                queue=self.queue.queue,
                durable=self.queue.durable,
            )
            logger.info(f"Queue {self.queue.queue} has been created")

    def delete_queue(self):
        with self._get_connection() as channel:
            channel.queue_delete(queue=self.queue.queue)


class RabbitConsumer(RabbitConnection):
    def __init__(self, creds: RabbitDataConnection, consumer: RabbitDataConsumer):
        assert isinstance(consumer, RabbitDataConsumer)
        super().__init__(creds)
        self.consumer = consumer

    def consume_messages(self):
        with self._get_connection() as channel:
            channel.basic_qos(prefetch_count=1)
            (
                method,
                properties,  # pylint: disable=unused-variable
                body,
            ) = channel.basic_get(
                queue=self.consumer.queue,
                auto_ack=self.consumer.auto_ack,
            )
            logger.info("Messages was consumed")
            return method.message_count, body

    def stop_consuming(self):
        with self._get_connection() as channel:
            channel.stop_consuming()
            logger.info("Consuming messages has been stopped")
