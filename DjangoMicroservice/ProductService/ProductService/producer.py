import json
import pika
import os
import uuid

HOST = os.environ.get("HOST", "localhost")
ROUTING_KEY = "django_microservice"
EXCHANGE = ""


class RPCProducer:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="localhost")
        )

        self.channel = self.connection.channel()

        print("===== Connected =====")

        result = self.channel.queue_declare(queue="", exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True,
        )

        self.response = None
        self.corr_id = None

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def publish(self, body: dict):
        self.response = None
        assert isinstance(body, dict), "`body` must be a dictionary"
        assert "action" in body, "`body` should have an action key"
        assert "data" in body, "`body` should have a data key"

        self.corr_id = str(uuid.uuid4())

        self.channel.basic_publish(
            exchange=EXCHANGE,
            routing_key=ROUTING_KEY,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=json.dumps(body),
        )

        while self.response is None:
            self.connection.process_data_events(time_limit=None)

        return json.loads(self.response)


producer = RPCProducer()
