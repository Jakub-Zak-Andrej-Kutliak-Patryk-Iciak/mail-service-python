import json
from json import JSONDecodeError
from typing import Optional, Callable

import pika


class MQService:

    def __init__(self, host: Optional[str] = None,
                 consumer_tag: str = "email-service",
                 queue_name: str = "mail_queue",
                 is_queue_durable: bool = True,
                 on_message_callback: Optional[Callable] = None):
        self.on_message_callback = on_message_callback
        self.is_queue_durable = is_queue_durable
        self.consumer_tag = consumer_tag
        self.connection = None
        self.channel = None

        if host:
            self.init_mq(host, queue_name)

    def init_mq(self,
                host: str,
                consumer_tag: str = "email-service",
                queue_name: str = "mail_queue",
                is_queue_durable: bool = True,
                on_message_callback: Optional[Callable] = None) -> None:
        if not host:
            raise Exception("Host parameter is required!")
        self.on_message_callback = on_message_callback
        self.is_queue_durable = is_queue_durable
        self.consumer_tag = consumer_tag
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host))
        self.channel = self.connection.channel()

        self._declare_queue(queue_name)

    def parse_message_body(self, body: bytearray) -> str:
        message = body
        try:
            my_json = body.decode('utf8').replace("'", '"')
            data = json.loads(my_json)
            message = json.dumps(data, indent=4, sort_keys=True)
        except JSONDecodeError as e:
            print(f'Message could not be parsed to json! Error={e}', )
        return message

    def _on_new_message(self, channel: any, method: any, properties: any, body: bytearray) -> None:
        print(f"Message:\nheaders={properties.headers},\ntext={self.parse_message_body(body)}")
        if self.on_message_callback is not None:
            self.on_message_callback()
        print('- ' * 20)

    def set_on_new_message_callback(self, callback: Callable) -> None:
        self.on_message_callback = callback

    def _declare_queue(self, queue_name: str) -> None:
        declare_result = self.channel.queue_declare(queue=queue_name,
                                                    durable=self.is_queue_durable,
                                                    auto_delete=not self.is_queue_durable)
        self._on_queue_declared(declare_result)
        print(f"Message queue {queue_name} initialized successfully!")

    def _on_queue_declared(self, declare_result: any) -> None:
        self.channel.basic_consume(consumer_tag=self.consumer_tag,
                                   on_message_callback=self._on_new_message,
                                   queue=declare_result.method.queue,
                                   auto_ack=True)

    def publish(self, queue_name: str = "mail_queue", message: str = "Empty message") -> None:
        self.channel.basic_publish(exchange="", routing_key=queue_name, body=message)

    def start_consuming(self) -> None:
        self.channel.start_consuming()
        print("Message queue is ready to consume!")

    def cancel_subscription(self) -> None:
        if not self.consumer_tag:
            raise Exception("Consumer tag parameter not specified")
        self.channel.basic_cancel(self.consumer_tag)
        self.connection.close()
        print("Unsubscribed successfully!")
