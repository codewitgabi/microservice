import pika
import os
import json

AMQP_HOST = os.environ.get("AMQP_HOST", "localhost")
EXCHANGE = os.environ.get("EXCHANGE", "")
ROUTING_KEY = os.environ.get("ROUTING_KEY", "")


class AMQPProducer:
    def __init__(self, *args, **kwargs):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="localhost")
        )
        print("[*] Connected to message broker")
        self.channel = self.connection.channel()

        self.channel.queue_declare(queue="task_queue", durable=True)

    def publish(self, body):
        body = json.loads(body)

        assert "action" in body, "body requires action attribute"
        assert "payload" in body, "body requires payload attribute"

        body = json.dumps(body)

        self.channel.basic_publish(
            exchange=EXCHANGE,
            routing_key=ROUTING_KEY,
            body=body,
            properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent),
        )


producer = AMQPProducer()
