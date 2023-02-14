from django.core.management.base import BaseCommand, CommandError
from rabbitmq.messages import MessageProcessing

class Command(BaseCommand):
    """
    This command runs the RabbitMQ consumer
    """
    help = 'Run the RabbitMQ consumer'

    def handle(self, *args, **options):
        # Instantiate a MessageProcessing object
        messages = MessageProcessing()
        # Call the consume method of the MessageProcessing object
        messages.consume()
