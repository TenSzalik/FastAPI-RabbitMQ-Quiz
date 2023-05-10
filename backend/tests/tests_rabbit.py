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
