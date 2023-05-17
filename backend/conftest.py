import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from core.endpoints.quiz import get_database
from core.models.database import Base
from core.models.models import Category, Answer, Question, Quiz, Result
from core.managers.rabbit_manager import (
    RabbitDataConnection,
    RabbitDataQueue,
    RabbitDataProducer,
    RabbitDataConsumer,
    RabbitQueue,
    RabbitProducer,
    RabbitConsumer,
)

POSTGRES_USERNAME = os.environ["POSTGRES_USERNAME"]
POSTGRES_PASSWORD = os.environ["POSTGRES_PASSWORD"]
POSTGRES_TEST_HOST = os.environ["POSTGRES_TEST_HOST"]
POSTGRES_TEST_DB = os.environ["POSTGRES_TEST_DB"]

RABBIT_USERNAME = os.environ["RABBIT_USERNAME"]
RABBIT_PASSWORD = os.environ["RABBIT_PASSWORD"]
RABBIT_HOST = os.environ["RABBIT_HOST"]

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_TEST_HOST}/{POSTGRES_TEST_DB}"
)

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
    database = TestingSessionLocal()
    category_1 = Category(name="category1")
    category_2 = Category(name="category2")

    answer_1 = Answer(name="answer1", value=-2)
    answer_2 = Answer(name="answer2", value=-1)
    answer_3 = Answer(name="answer3", value=0)
    answer_4 = Answer(name="answer4", value=1)
    answer_5 = Answer(name="answer5", value=2)

    question_1 = Question(name="question1")
    question_2 = Question(name="question2")

    database.add_all(
        [
            category_1,
            category_2,
            answer_1,
            answer_2,
            answer_3,
            answer_4,
            answer_5,
            question_1,
            question_2,
        ]
    )
    database.commit()

    quiz_1 = Quiz(
        category=category_1,
        answer=[answer_1, answer_2, answer_3, answer_4, answer_5],
        question=question_1,
    )

    quiz_2 = Quiz(
        category=category_2,
        answer=[answer_1, answer_2, answer_3, answer_4, answer_5],
        question=question_2,
    )

    result = Result(age=24, sex="Male", quiz="{category_1: 2, category_2: 2}")

    database.add_all([quiz_1, quiz_2, result])
    database.commit()


@pytest.fixture
def rabbit_load_creds():
    creds = RabbitDataConnection(
        username=RABBIT_USERNAME, password=RABBIT_PASSWORD, host=RABBIT_HOST
    )
    return creds


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
