import pika
from django.conf import settings

def connect():
    credentials = pika.PlainCredentials(settings.RABBITMQ_USER, settings.RABBITMQ_PASSWORD)
    connection = pika.BlockingConnection(pika.ConnectionParameters(settings.RABBITMQ_HOST, credentials=credentials))
    channel = connection.channel()
    return channel
