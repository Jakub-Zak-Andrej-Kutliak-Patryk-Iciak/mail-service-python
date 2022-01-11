def test_mq_connection_and_ability_to_publish_and_consume(test_mq_service):
    host = "localhost"
    queue_name = "test_mail_queue"
    consumer_tag = "test-email-service"
    test_message = '{ "message": "Hey there, this is a test message!" }'
    print("Testing mq connection")
    """
    GIVEN a mq service
    WHEN connected and published-received a message
    THEN should parse and print out the message and close channel immediately 
    """
    test_mq_service.init_mq(host=host, consumer_tag=consumer_tag, queue_name=queue_name, is_queue_durable=False)
    test_mq_service.set_on_new_message_callback(test_mq_service.cancel_subscription)
    test_mq_service.publish(queue_name=queue_name, message=test_message)
    test_mq_service.start_consuming()

