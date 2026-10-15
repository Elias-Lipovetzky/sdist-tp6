import os
import sys
import pika
from dotenv import load_dotenv

load_dotenv()

host = os.getenv("RABBITMQ_HOST", "localhost")
user = os.getenv("RABBITMQ_USER", "guest")
password = os.getenv("RABBITMQ_PASSWORD", "guest")

credentials = pika.PlainCredentials(user, password)

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host=host,
        credentials=credentials
    )
)

channel = connection.channel()

channel.exchange_declare(
    exchange="stock_ex",
    exchange_type="topic"
)

binding_key = sys.argv[1]

result = channel.queue_declare(
    queue="",
    exclusive=True
)

queue_name = result.method.queue

channel.queue_bind(
    exchange="stock_ex",
    queue=queue_name,
    routing_key=binding_key
)


def recibir(ch, method, properties, body):
    print(
        f"[{binding_key}] "
        f"{method.routing_key} -> {body.decode()}"
    )


channel.basic_consume(
    queue=queue_name,
    on_message_callback=recibir,
    auto_ack=True
)

print(f"Suscripto a: {binding_key}")
channel.start_consuming()
