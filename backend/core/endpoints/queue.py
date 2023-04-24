from fastapi import Cookie, APIRouter
from fastapi.encoders import jsonable_encoder
from core.rabbimq.rabbit_manager import (
    RabbitDataQueue,
    RabbitQueue,
    RabbitDataProducer,
    RabbitProducer,
    RabbitDataConnection,
)
from core.chart.chart_manager import DataCategoryChart, DataPointsChart, GenerateChart
from core.utils.get_sum_dicts import get_sum_dicts
from core.utils.consume_queue import consume_queue

router = APIRouter(
    prefix="/queue",
    tags=["queue"],
    responses={404: {"description": "Not found"}},
)


@router.get("/create/")
def create_queue(queue: str = Cookie(None)):
    creds = RabbitDataConnection(
        username="guest", password="guest1234", host="localhost"
    )
    queue_data = RabbitDataQueue(queue=queue, durable=True)
    RabbitQueue(creds=creds, queue=queue_data).create_queue()
    return {"queue": queue}


@router.post("/send/")
def send_to_queue(answer, queue: str = Cookie(None)):
    creds = RabbitDataConnection(
        username="guest", password="guest1234", host="localhost"
    )
    body = jsonable_encoder(answer)
    producer_data = RabbitDataProducer("", routing_key=queue, body=str(body))
    RabbitProducer(creds=creds, producer=producer_data).send()
    return answer
