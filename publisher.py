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

routing_key = sys.argv[1]
mensaje = sys.argv[2]

channel.basic_publish(
    exchange="stock_ex",
    routing_key=routing_key,
    body=mensaje
)

print(f"Publicado [{routing_key}]: {mensaje}")

connection.close()
