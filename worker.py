import os
import sys
import time
import pika
from dotenv import load_dotenv

load_dotenv()

host = os.getenv("RABBITMQ_HOST", "localhost")
user = os.getenv("RABBITMQ_USER", "guest")
password = os.getenv("RABBITMQ_PASSWORD", "guest")

worker_name = sys.argv[1]

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

channel.basic_qos(
    prefetch_count=1
)


def procesar(ch, method, properties, body):
    mensaje = body.decode()

    print(f"[{worker_name}] Recibida: {mensaje}")

    segundos = mensaje.count(".")
    time.sleep(segundos)

    print(f"[{worker_name}] Terminada: {mensaje}")

    ch.basic_ack(
        delivery_tag=method.delivery_tag
    )


channel.basic_consume(
    queue="tareas",
    on_message_callback=procesar,
    auto_ack=False
)

print(f"[{worker_name}] Esperando tareas...")
channel.start_consuming()
