import pika
import os
from dotenv import load_dotenv

load_dotenv()

credentials = pika.PlainCredentials(
    os.getenv("RABBITMQ_USER", "guest"),
    os.getenv("RABBITMQ_PASSWORD", "guest")
)

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host=os.getenv("RABBITMQ_HOST", "localhost"),
        credentials=credentials
    )
)

channel = connection.channel()
channel.queue_declare(queue="tareas", durable=True)

channel.basic_publish(
    exchange="",
    routing_key="tareas",
    body="Tarea que va a fallar.........."
)

connection.close()
