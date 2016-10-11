import json
import pika
import random

def consumer():
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
    channel = connection.channel()

    #retry queue
    channel.exchange_declare(exchange='worker_exchange',type='fanout')

    result = channel.queue_declare(exclusive=True)

    queue_name = result.method.queue

    channel.queue_bind(exchange='worker_exchange',
                   queue=queue_name)

    channel.queue_bind(exchange='retry_exchange',
                    queue='retry_queue')

    print 'Waiting for logs. To exit press CTRL+C'

    def callback(ch, method, properties, body):
        print(" [x] %r" % body)
        channel.basic_publish(exchange='retry_exchange',
                          routing_key='',
                          body='Hello World1')

    channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

    channel.start_consuming()

consumer()
