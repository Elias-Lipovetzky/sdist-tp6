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


def recibir(ch, method, properties, body):
    print(f"Recibido: {body.decode()}")


channel.basic_consume(
    queue="hola",
    on_message_callback=recibir,
    auto_ack=True
)

print("Esperando mensajes... CTRL+C para salir.")

channel.start_consuming()
