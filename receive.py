#!/usr/bin/env python
import pika
import time

credentials = pika.PlainCredentials('guest', 'guest')
parameters = pika.ConnectionParameters('localhost', 30002, '/', credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.exchange_declare(exchange='sendlogs', exchange_type='fanout')
channel.queue_declare(queue='logs')
channel.queue_bind(queue='logs', exchange='sendlogs')

def callback(ch, method, properties, body):
    value = body.decode('UTF-8')
    print(f"{value}\t{int(round(time.time() * 1000))}")

channel.basic_consume(queue='logs', on_message_callback=callback, auto_ack=True)

channel.start_consuming()
print(' [*] Waiting for logs. To exit press CTRL+C')
