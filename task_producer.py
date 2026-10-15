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

channel.queue_declare(
    queue="tareas",
    durable=True
)

cantidad = int(sys.argv[1])

for i in range(1, cantidad + 1):
    puntos = "." * ((i % 3) + 1)
    mensaje = f"Tarea {i}{puntos}"

    channel.basic_publish(
        exchange="",
        routing_key="tareas",
        body=mensaje,
        properties=pika.BasicProperties(
            delivery_mode=2
        )
    )

    print(f"Enviada: {mensaje}")

connection.close()
