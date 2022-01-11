import json
from json import JSONDecodeError

import pika
import threading


class ConsumerThread(threading.Thread):
    def __init__(self, host, *args, **kwargs):
        super(ConsumerThread, self).__init__(*args, **kwargs)

        self._host = host

    # Not necessarily a method.
    def callback_func(self, channel, method, properties, body):
        print(f"{self.name} received '{body}'")

    def run(self):
        # credentials = pika.PlainCredentials("guess", "guess")

        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self._host,
                                      # credentials=credentials
                                      ))

        channel = connection.channel()

        result = channel.queue_declare(queue='mail_queue', durable=True)

        # channel.queue_bind(result.method.queue,
        #                    exchange="my-exchange",
        #                    routing_key="*.*.*.*.*")

        channel.basic_consume(on_message_callback=self.callback_func,
                              queue=result.method.queue,
                              auto_ack=True)

        channel.start_consuming()


class ConsumerWithoutThread:

    def __init__(self, host):
        self._host = host
        self.connection = None
        self.channel = None

    def callback_func(self, channel, method, properties, body):
        print('- ' * 20)
        message = body
        try:
            my_json = body.decode('utf8').replace("'", '"')
            data = json.loads(my_json)
            message = json.dumps(data, indent=4, sort_keys=True)
        except JSONDecodeError as e:
            print(f'Message could not be parsed to json! Error={e}',)
        print(f"Received new message: channel={channel},\n method={method},\n properties={properties.headers},\n body={message}")
        received_messages_during_cancel = self.channel.basic_cancel("email-consumer")
        print("cancel result", received_messages_during_cancel)
        self.connection.close()

    def consume(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self._host))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='mail_queue', durable=True, auto_delete=False)

        self.channel.basic_consume(consumer_tag="email-consumer",
                                   on_message_callback=self.callback_func,
                                   queue=result.method.queue,
                                   auto_ack=True)

        self.channel.start_consuming()

        # cancel_result = self.channel.basic_cancel("email-consumer")
        # self.connection.close()


if __name__ == "__main__":
    thread = ConsumerThread("localhost")
    thread2 = ConsumerWithoutThread("localhost")
    # thread.start()
    thread2.consume()
