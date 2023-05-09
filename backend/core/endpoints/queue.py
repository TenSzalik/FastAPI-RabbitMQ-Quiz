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


@router.post("/create/", response_model=QueueCreateSchema)
def create_queue(queue: QueueCreateSchema):
    creds = RabbitDataConnection(
        username="guest", password="guest1234", host="localhost"
    )
    queue_data = RabbitDataQueue(queue=queue.queue, durable=True)
    RabbitQueue(creds=creds, queue=queue_data).create_queue()
    return {"queue": queue.queue}


@router.post("/send/", response_model=QueueSchema)
def send_to_queue(answer: QueueSchema):
    creds = RabbitDataConnection(
        username="guest", password="guest1234", host="localhost"
    )
    body = jsonable_encoder(answer)
    producer_data = RabbitDataProducer(
        "", routing_key=body["queue"], body=str({body["category"]: body["answer"]})
    )
    RabbitProducer(creds=creds, producer=producer_data).send()
    return {"queue": answer.queue, "category": answer.category, "answer": answer.answer}


@router.delete("/", response_model=QueueCreateSchema)
def delete_queue(queue: QueueCreateSchema):
    creds = RabbitDataConnection(
        username="guest", password="guest1234", host="localhost"
    )
    queue_data = RabbitDataQueue(queue=queue.queue, durable=True)
    RabbitQueue(creds=creds, queue=queue_data).delete_queue()
    return {"queue": queue.queue}


@router.post("/consume/")
def consume_queue(queue: QueueCreateSchema):
    quiz_raw_data = []
    creds = RabbitDataConnection(
        username="guest", password="guest1234", host="localhost"
    )
    consumer_data = RabbitDataConsumer(queue=queue.queue, auto_ack=True)
    consumer = RabbitConsumer(creds=creds, consumer=consumer_data)
    count, message = consumer.consume_messages()
    quiz_raw_data.append(loads(message.decode().replace("'", '"')))
    for number_of_messages in range(count):  # pylint: disable=unused-variable
        count, message = consumer.consume_messages()
        quiz_raw_data.append(loads(message.decode().replace("'", '"')))
    return get_sum_dicts(quiz_raw_data)
