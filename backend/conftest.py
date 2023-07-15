from datetime import timedelta
import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from core.endpoints.quiz import get_database
from core.models.database import Base
from core.managers.rabbit_manager import (
    RabbitDataConnection,
    RabbitDataQueue,
    RabbitDataProducer,
    RabbitDataConsumer,
    RabbitQueue,
    RabbitProducer,
    RabbitConsumer,
)
from core.utils.load_simple_db import load_simple_db
from core.endpoints.token import create_access_token


POSTGRES_USERNAME = os.environ["POSTGRES_USERNAME"]
POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]
POSTGRES_TEST_HOST = os.environ["POSTGRES_TEST_HOST"]
POSTGRES_TEST_DB = os.environ["POSTGRES_TEST_DB"]

RABBIT_USERNAME = os.environ["RABBIT_USERNAME"]
RABBIT_PASSWORD = os.environ["RABBIT_PASSWORD"]
RABBIT_HOST = os.environ["RABBIT_HOST"]

SQLALCHEMY_DATABASE_URL = f"postgresql://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_TEST_HOST}/{POSTGRES_TEST_DB}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_database():
    try:
        database = TestingSessionLocal()
        yield database
    finally:
        database.close()


app.dependency_overrides[get_database] = override_get_database
client = TestClient(app)


@pytest.fixture()
def run_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def load_database():
    load_simple_db(TestingSessionLocal())


@pytest.fixture(name="rabbit_load_creds")
def fixture_rabbit_load_creds():
    creds = RabbitDataConnection(
        username=RABBIT_USERNAME, password=RABBIT_PASSWORD, host=RABBIT_HOST
    )
    return creds


@pytest.fixture
def token_header():
    return {
        "Authorization": "Bearer "
        + create_access_token(
            data={"sub": "foobarbaz@gmail.com"}, expires_delta=timedelta(minutes=30)
        ),
        "token_type": "bearer",
    }


@pytest.fixture
def rabbit_load_queue(rabbit_load_creds):
    queue_data = RabbitDataQueue(queue="test", durable=False)
    queue = RabbitQueue(creds=rabbit_load_creds, queue=queue_data)
    return queue


@pytest.fixture
def rabbit_load_producer(rabbit_load_creds):
    producer_data = RabbitDataProducer("", routing_key="test", body="foo")
    producer = RabbitProducer(creds=rabbit_load_creds, producer=producer_data)
    return producer


@pytest.fixture
def rabbit_load_consumer(rabbit_load_creds):
    consumer_data = RabbitDataConsumer(queue="test", auto_ack=True)
    consumer = RabbitConsumer(creds=rabbit_load_creds, consumer=consumer_data)
    return consumer
