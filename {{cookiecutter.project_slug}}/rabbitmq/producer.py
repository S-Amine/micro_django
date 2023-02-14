import json
from django.conf import settings
from rabbitmq.rabbitmq_connector import connect

def publish(message):
    """ Publish a message to the RabbitMQ Exchange """
    # connect to the RabbitMQ channel
    channel = connect()
    # get the exchange type from settings
    exchange_type = settings.RABBITMQ_EXCHANGE_TYPE
    # get the exchange name from settings
    exchange = settings.RABBITMQ_EXCHANGE
    # get the routing key from settings
    routing_key = settings.RABBITMQ_ROUTING_KEY
    # declare the exchange on the channel
    channel.exchange_declare(exchange=exchange, exchange_type=exchange_type)
    # publish the message to the exchange
    channel.basic_publish(exchange=exchange, routing_key=routing_key, body=json.dumps(message))
