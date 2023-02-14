from django.conf import settings
from rabbitmq.rabbitmq_connector import connect
import time
from {{cookiecutter.project_slug}}.utils import colors

class Consume:
    def __init__(self, callback):
        self.callback = callback
        self.channel, self.queue_name = self.connect_to_rabbitmq()
        self.should_reconnect = False

    def connect_to_rabbitmq(self):
        print(f"{colors['white']}\n\n\nWelcome! In this process, we will be connecting to the RabbitMQ broker to consume messages from the queue\033[0m")
        print(f"{colors['white']}\nThe Broker address is :{colors['cyan']} {settings.RABBITMQ_HOST}\033[0m")
        print(f"{colors['white']}The RabbitMQ user is :{colors['cyan']} {settings.RABBITMQ_USER}\033[0m")
        print(f"{colors['white']}The RabbitMQ exchange is :{colors['cyan']} {settings.RABBITMQ_EXCHANGE}\033[0m")
        print(f"{colors['white']}The RabbitMQ exchange type :{colors['cyan']} {settings.RABBITMQ_EXCHANGE_TYPE}\033[0m")
        print(f"{colors['white']}The RabbitMQ routing key is :{colors['cyan']} {settings.RABBITMQ_ROUTING_KEY}\033[0m")
        print(f"{colors['white']}The RabbitMQ queue :{colors['cyan']} {settings.RABBITMQ_QUEUE}\033[0m")
        print(f"{colors['white']}\nIn your Django settings file, you can modify the RabbitMq variables.\033[0m")
        time.sleep(2)
        while True:
            try:
                # Connect to RabbitMQ queue
                print(f"{colors['cyan']}\nConnecting to the RabbitMQ Broker ...\033[0m")
                channel = connect()
                print(f"{colors['green']}\nWelcome! You have successfully connected to the RabbitMQ broker and are now ready to consume messages from the queue. Let's get started!\033[0m")
                # Declare queue
                queue = channel.queue_declare(queue=settings.RABBITMQ_QUEUE, durable=True, exclusive=False, auto_delete=False)
                queue_name = queue.method.queue
                # Declare exchange
                channel.exchange_declare(
                    exchange=settings.RABBITMQ_EXCHANGE,
                    exchange_type=settings.RABBITMQ_EXCHANGE_TYPE
                )
                # Bind queue and exchange with routing key
                channel.queue_bind(
                    exchange=settings.RABBITMQ_EXCHANGE,
                    queue=queue_name,
                    routing_key=settings.RABBITMQ_ROUTING_KEY
                )
                self.should_reconnect = False
                return channel, queue_name
            except Exception as ex:
                self.should_reconnect = True
                print(f"{colors['red']}\nError while trying to connect to RabbitMQ. Retrying in 5 seconds...\033[0m")
                time.sleep(5)
                continue

    def consume(self):
        while self.should_reconnect:
            self.channel, self.queue_name = self.connect_to_rabbitmq()
        # Set up callback
        self.channel.basic_consume(on_message_callback=self.callback, queue=self.queue_name)
        # Start consuming messages
        self.channel.start_consuming()
