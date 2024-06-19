import pika

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

# result = channel.queue_declare(queue="world", durable=True)
channel.exchange_declare(exchange="logs", exchange_type="fanout", durable=True)


def send_message():
    message = input("Enter message: ")

    channel.basic_publish(
        exchange="logs",
        routing_key="world",
        body=message,
        properties=pika.BasicProperties(delivery_mode=pika.DeliveryMode.Persistent),
    )


if __name__ == "__main__":
    send_message()
    connection.close()
