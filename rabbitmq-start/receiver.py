# /usr/bin/env python
"""
    * ref => https://www.rabbitmq.com/tutorials/tutorial-one-python
"""

import pika
from time import sleep

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()  # create connection to a broker (rabbitmq server)

print("========== Connected ==========")
channel.queue_declare(
    queue="hello", durable=True
)  # create a queue where our messages will be sent to. This is idempotent. Only one is created no matter the number of times it is called


def callback(ch, method, properties, body):
    print(f" [x] Received {body.decode()}")
    sleep(body.count(b"."))
    print(" [x] Done")
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue="hello", on_message_callback=callback)

channel.start_consuming()
