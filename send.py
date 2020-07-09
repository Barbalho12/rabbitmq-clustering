#!/usr/bin/env python
import pika
import sys
import time
import threading

credentials = pika.PlainCredentials('guest', 'guest')
parameters = pika.ConnectionParameters('localhost', 30002, '/', credentials)

def sender(id_thread):
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    for i in range(1000):
        message = i*id_thread
        channel.basic_publish(exchange='sendlogs', routing_key='alo',  body=str(message))
        # time.sleep(0.1)
        print(f"{message}\t{int(round(time.time() * 1000))}")
    connection.close()

threads = []
for i in range(100):
    t = threading.Thread(target=sender, args=(i,), daemon=False)
    threads.append(t)
    t.start()
    
for t in threads:
    t.join()
