import pika
import os
import json

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
django.setup()

from django.contrib.auth import get_user_model
from django.forms.models import model_to_dict
from rest_framework_simplejwt.tokens import AccessToken
from django.core import serializers


User = get_user_model()

HOST = os.environ.get("BROKER_HOST", "localhost")
QUEUE = "django_microservice"
EXCHANGE = ""

ACTIONS = ["is_valid_user_id", "authenticate"]

connection = pika.BlockingConnection(pika.ConnectionParameters(host=HOST))
channel = connection.channel()

print("===== Connected =====")

channel.queue_declare(queue=QUEUE, durable=True)


def callback(ch, method, props, body: str):
    body = json.loads(body.decode("utf-8"))

    action = body.get("action")
    data = json.loads(body.get("data"))

    assert action in ACTIONS, f"action must be one of {ACTIONS}"
    response = None

    match action:
        case "is_valid_user_id":
            vendor_id: int = data.get("vendor")
            response = User.objects.filter(id=vendor_id).exists()

        case "authenticate":
            token: str = data.get("token")

            try:
                claim = AccessToken(token)
                response = User.objects.values(
                    "id", "username", "email", "first_name", "last_name"
                ).get(id=claim.get("user_id"))

            except Exception as e:
                response = str(e)

        case _:
            raise Exception("Invalid action")

    ch.basic_publish(
        exchange=EXCHANGE,
        routing_key=props.reply_to,
        properties=pika.BasicProperties(correlation_id=props.correlation_id),
        body=json.dumps(
            {
                "data": response,
            }
        ),
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=QUEUE, on_message_callback=callback)

print("===== Started consuming =====")

channel.start_consuming()
