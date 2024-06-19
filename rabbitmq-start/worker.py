import pika
import time

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

print("===== Connected =====")

channel.exchange_declare(exchange="logs", exchange_type="fanout")
result = channel.queue_declare(queue="world", exclusive=True)
channel.queue_bind(exchange="logs", queue=result.method.queue)

def callback(ch, method, properties, body):
    message = body.decode("utf-8")
    time.sleep(len(message))
    print(f"[x] Received {body.decode("utf-8")}")
    ch.basic_ack(delivery_tag = method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='world',
                      on_message_callback=callback)
channel.start_consuming()
