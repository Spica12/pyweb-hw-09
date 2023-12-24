import json
import random
from datetime import datetime

import pika
from faker import Faker

from models import Contact

fake = Faker("uk-UA")

credentials = pika.PlainCredentials(username="guest", password="guest")

connection = pika.BlockingConnection(
    pika.ConnectionParameters("localhost", port=5672, credentials=credentials)
)
channel = connection.channel()

exchange = "pyweb-hw-08 Service"
queue_sms = "pyweb-hw-08_sms"
queue_email = "pyweb-hw-08_email"


channel.exchange_declare(exchange=exchange, exchange_type="direct")

channel.queue_declare(queue=queue_sms, durable=True)
channel.queue_bind(exchange=exchange, queue=queue_sms)

channel.queue_declare(queue=queue_email, durable=True)
channel.queue_bind(exchange=exchange, queue=queue_email)


def create_tasks(nums: int):
    for i in range(nums):
        contact = Contact(
            fullname=fake.name(),
            phone=fake.phone_number(),
            type_of_delivery=random.choice(['sms', 'email']),
            email=fake.email(),
        ).save()

        channel.basic_publish(
            exchange=exchange,
            routing_key=queue_email if contact.type_of_delivery == 'email' else queue_sms,
            body=str(contact.id).encode(),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            ),
        )
        print(f" [x] Sent '{contact.id}'")

    connection.close()


if __name__ == "__main__":
    create_tasks(10)
