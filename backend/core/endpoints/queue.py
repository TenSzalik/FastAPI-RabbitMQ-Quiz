import os
from json import loads
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from core.managers.rabbit_manager import (
    RabbitDataQueue,
    RabbitQueue,
    RabbitDataProducer,
    RabbitProducer,
    RabbitDataConnection,
    RabbitDataConsumer,
    RabbitConsumer,
)
from core.models.schemas import QueueSchema, QueueCreateSchema
from core.utils.get_sum_dicts import get_sum_dicts

router = APIRouter(
    prefix="/queue",
    tags=["queue"],
    responses={404: {"description": "Not found"}},
)

RABBIT_USERNAME = os.environ["RABBIT_USERNAME"]
RABBIT_PASSWORD = os.environ["RABBIT_PASSWORD"]
RABBIT_HOST = os.environ["RABBIT_HOST"]


@router.post("/create/", response_model=QueueCreateSchema)
def create_queue(queue: QueueCreateSchema):
    creds = RabbitDataConnection(
        username=RABBIT_USERNAME, password=RABBIT_PASSWORD, host=RABBIT_HOST
    )
    queue_data = RabbitDataQueue(queue=queue.queue, durable=True)
    RabbitQueue(creds=creds, queue=queue_data).create_queue()
    return {"queue": queue.queue}


@router.post("/send/", response_model=QueueSchema)
def send_to_queue(answer: QueueSchema):
    creds = RabbitDataConnection(
        username=RABBIT_USERNAME, password=RABBIT_PASSWORD, host=RABBIT_HOST
    )
    body = jsonable_encoder(answer)
    producer_data = RabbitDataProducer(
        "", routing_key=body["queue"], body=str({body["category"]: body["answer"]})
    )
    RabbitProducer(creds=creds, producer=producer_data).send()
    return {"queue": answer.queue, "category": answer.category, "answer": answer.answer}


@router.post("/delete/", response_model=QueueCreateSchema)
def delete_queue(queue: QueueCreateSchema):
    creds = RabbitDataConnection(
        username=RABBIT_USERNAME, password=RABBIT_PASSWORD, host=RABBIT_HOST
    )
    queue_data = RabbitDataQueue(queue=queue.queue, durable=True)
    RabbitQueue(creds=creds, queue=queue_data).delete_queue()
    return {"queue": queue.queue}


@router.post("/consume/")
def consume_queue(queue: QueueCreateSchema):
    quiz_raw_data = []
    creds = RabbitDataConnection(
        username=RABBIT_USERNAME, password=RABBIT_PASSWORD, host=RABBIT_HOST
    )
    consumer_data = RabbitDataConsumer(queue=queue.queue, auto_ack=True)
    consumer = RabbitConsumer(creds=creds, consumer=consumer_data)
    count, message = consumer.consume_messages()
    quiz_raw_data.append(loads(message.decode().replace("'", '"')))
    for _ in range(count):  # pylint: disable=unused-variable
        count, message = consumer.consume_messages()
        quiz_raw_data.append(loads(message.decode().replace("'", '"')))
    return get_sum_dicts(quiz_raw_data)
