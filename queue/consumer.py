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

    queue_name = 'worker_queue'#result.method.queue

    print "queue_name is",queue_name

    channel.queue_bind(exchange='worker_exchange',
                   queue=queue_name)

    channel.queue_bind(exchange='retry_exchange',
                    queue='retry_queue')

    print 'Waiting for logs. To exit press CTRL+C'

    def callback(ch, method, properties, body):
        print(" [x] %r" % body)
        if random.random() < 0.5:
            print "enque retry queue",method.delivery_tag
            channel.basic_publish(exchange='retry_exchange',
                              routing_key='',
                              body=body)
        else:
            print "ack message",method.delivery_tag
            ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

    channel.start_consuming()

consumer()
