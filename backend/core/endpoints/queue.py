from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from core.rabbimq.rabbit_manager import (
    RabbitDataQueue,
    RabbitQueue,
    RabbitDataProducer,
    RabbitProducer,
    RabbitDataConnection,
)
from core.schemas.schemas import QueueSchema, QueueCreateSchema

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
