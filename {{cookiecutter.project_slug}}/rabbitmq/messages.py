from rabbitmq.consumer import Consume
import json
from datetime import datetime
from {{cookiecutter.project_slug}}.utils import colors

class MessageProcessing(Consume):
    """A class for processing messages from RabbitMQ"""

    def default_callback(self, ch, method, proterties, body):
        """
        Default callback for processing messages from RabbitMQ.
        Loads the message body as JSON, prints it, and acknowledges the message.
        """
        now = datetime.now()
        print(f"{colors['white']}\n{now} New message ==> {json.loads(body)}\033[0m")
        message = json.loads(body)
        # Do whatever you want with messages here

        # This line is important to consume messages and do not receive them again
        ch.basic_ack(delivery_tag=method.delivery_tag)


    def __init__(self, callback=None):
        """
        Initialize the MessageProcessing class.
        If no callback is provided, the default_callback method is used.
        """
        if not callback:
            callback = self.default_callback
        super().__init__(callback)
