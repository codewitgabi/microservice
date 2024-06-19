# /usr/bin/env python
"""
    * ref => https://www.rabbitmq.com/tutorials/tutorial-one-python
"""

import pika, sys

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()  # create connection to a broker (rabbitmq server)

print("========== Connected ==========")
channel.queue_declare(
    queue="hello", durable=True
)  # create a queue where our messages will be sent to


"""
In RabbitMQ a message can never be sent directly to the queue, it always needs to go through an exchange.
"""

"""
    * exchange => The exchange for our broker
    * routing_key => The queue we want our messages to be sent
    * body => The message body
"""

message = " ".join(sys.argv[1:]) or "Hello, world!"
channel.basic_publish(
    exchange="",
    routing_key="hello",
    body=message,
    properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent),
)

print(f" [x] Sent {message}")

connection.close()  # flush network buffers.
