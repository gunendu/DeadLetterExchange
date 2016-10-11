import json
import pika
import random
import requests

def consumer():
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
    channel = connection.channel()

    #retry queue
    channel.exchange_declare(exchange='worker_exchange',type='fanout')

    #result = channel.queue_declare(exclusive=True)

    queue_name = 'worker_queue' #result.method.queue

    channel.queue_bind(exchange='worker_exchange',
                   queue=queue_name)

    channel.queue_bind(exchange='retry_exchange',
                    queue='retry_queue')

    def callback(ch, method, properties, body):
        body = json.loads(body)
        data = {}
        data['message'] = body['msg']
        url = body['url']
        response = requests.post(url,json.dumps(data))
        if response.status_code == 400:
            print "retry_exchange ",data['message']
            channel.basic_publish(exchange='retry_exchange',
                         routing_key='',
                         body=json.dumps(body))
        else:
            print "ack for message ",data['message']


    channel.basic_consume(callback,
                      queue=queue_name,
                      no_ack=True)

    channel.start_consuming()

consumer()
