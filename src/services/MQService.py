import json
import threading
from json import JSONDecodeError
from typing import Optional, Callable

import pika

from src.services import EmailService


class MQService(threading.Thread):

    def __init__(self,
                 connect_url: str = None,
                 app: Optional[any] = None,
                 consumer_tag: str = "email-service",
                 queue_name: str = "mail-queue",
                 is_queue_durable: bool = True,
                 on_message_callback: Optional[Callable] = None,
                 *args, **kwargs):
        super(MQService, self).__init__(*args, **kwargs)
        self.on_message_callback = on_message_callback
        self.is_queue_durable = is_queue_durable
        self.consumer_tag = consumer_tag
        self.queue_name = queue_name
        self.connection = None
        self.channel = None
        self.app = app

        if connect_url:
            self.init_mq(connect_url=connect_url, app=app, queue_name=queue_name)

    def init_mq(self,
                app: any,
                connect_url: str,
                queue_name: str,
                consumer_tag: str = "email-service",
                is_queue_durable: bool = True,
                on_message_callback: Optional[Callable] = None) -> None:
        if not connect_url:
            raise Exception("Connect string parameter is required!")
        self.app = app
        self.consumer_tag = consumer_tag
        self.is_queue_durable = is_queue_durable
        self.on_message_callback = on_message_callback

        if connect_url:
            self.connect(connect_url=connect_url, queue_name=queue_name)

    def connect(self, connect_url: str, queue_name: str):
        self.connection = pika.BlockingConnection(pika.URLParameters(connect_url))
        self.channel = self.connection.channel()
        self._declare_queue(queue_name)

    def parse_message_body(self, body: bytearray) -> tuple[Optional[dict], Optional[str]]:
        message = body
        error = None
        try:
            my_json = body.decode('utf8').replace("'", '"')
            message = json.loads(my_json)
        except JSONDecodeError as e:
            error = f'Message could not be parsed to json! Error={e}'
        return message, error

    def _on_new_message(self, channel: any, method: any, properties: any, body: bytearray) -> None:
        print('- ' * 20)
        body_json, error = self.parse_message_body(body)
        if error:
            print(f"An error was raised while paring message body:\nERROR => {error}\nBODY CONTENT => {body.decode('utf8')}")
            return

        print(f"Message:\nheaders={properties.headers},\ntext={json.dumps(body_json, indent=4, sort_keys=True)}")
        message, error = EmailService.parse_request_to_message(body_json)
        if error:
            print(f"An error was raised while paring message:\nERROR => {error}")
            return

        if self.on_message_callback is not None:
            self.on_message_callback(message)
        # channel.basic_ack(delivery_tag=method.delivery_tag)

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
        self.start()

    def publish(self, queue_name: str = "mail-queue", message: str = "Empty message") -> None:
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

    def run(self) -> None:
        with self.app.app_context():
            print("Message queue is ready to consume!")
            self.channel.start_consuming()
