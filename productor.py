import os
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

channel.queue_declare(queue="hola")

mensaje = "Hola RabbitMQ"

channel.basic_publish(
    exchange="",
    routing_key="hola",
    body=mensaje
)

print(f"Enviado: {mensaje}")

connection.close()
