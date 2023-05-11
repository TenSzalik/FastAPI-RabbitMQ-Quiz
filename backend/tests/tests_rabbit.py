"""
Tests that perform operations on RabbitMQ are not isolated - this means that
the execution of tests requires the rabbit server to be enabled.
The order of test execution is crucial.
"""
import pytest
import pika
from conftest import client


def test_rabbit_manager(rabbit_load_queue, rabbit_load_producer, rabbit_load_consumer):
    rabbit_load_queue.create_queue()
    rabbit_load_producer.send()
    count, message = rabbit_load_consumer.consume_messages()
    rabbit_load_queue.delete_queue()

    (
        queue_check_channel,
        queue_check_connection,
    ) = rabbit_load_queue.check_is_channel_and_connection_open()
    (
        producer_check_channel,
        producer_check_connection,
    ) = rabbit_load_producer.check_is_channel_and_connection_open()
    (
        consumer_check_channel,
        consumer_check_connection,
    ) = rabbit_load_consumer.check_is_channel_and_connection_open()
    assert count == 0
    assert message == b"foo"
    assert queue_check_channel, queue_check_connection == True
    assert producer_check_channel, producer_check_connection == True
    assert consumer_check_channel, consumer_check_connection == True


def test_create_queue():
    """
    Queue creation is idempotent - a queue with the same properties
    and the same name will not be created if it already exists.
    """
    data = {"queue": "foo"}
    response = client.post("/queue/create/", json=data)
    assert response.status_code == 200
    assert response.json() == data


def test_send_to_queue():
    data = {"queue": "foo", "category": "bar", "answer": 1}
    response = client.post("/queue/send/", json=data)
    assert response.status_code == 200
    assert response.json() == data


def test_consume_queue():
    data = {"queue": "foo"}
    response = client.post("/queue/consume/", json=data)
    assert response.status_code == 200
    assert response.json() == {"bar": 1}


def test_consume_empty_queue():
    data = {"queue": "foo"}
    with pytest.raises(
        AttributeError, match="'NoneType' object has no attribute 'message_count'"
    ):
        client.post("/queue/consume/", json=data)


def test_delete_queue():
    """
    This test does not check whether the queue has been
    removed but whether the endpoint is working.
    Removing the queue checks the next test - test_consume_queue_after_deleting_queue.
    It is possible to check directly if the queue has been deleted
    by adding a callback in the queue_delete function in core/managers/rabbit_manager.py
    but this way is just as effective and much simpler.
    """
    data = {"queue": "foo"}
    response = client.post("/queue/delete/", json=data)
    assert response.status_code == 200
    assert response.json() == data


def test_consume_queue_after_deleting_queue():
    data = {"queue": "foo"}
    with pytest.raises(
        pika.exceptions.ChannelClosedByBroker,
        match="(404, \"NOT_FOUND - no queue 'foo' in vhost '/'\")",
    ):
        client.post("/queue/consume/", json=data)
