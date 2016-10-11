import json
import pika,os,urlparse
import random
import requests

def consumer():
    #connection = pika.BlockingConnection(pika.ConnectionParameters(
    #    host='localhost'))

    #Heroku changes start

    url_str = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost//')
    url = urlparse.urlparse(url_str)
    params = pika.ConnectionParameters(host=url.hostname, virtual_host=url.path[1:],
             credentials=pika.PlainCredentials(url.username, url.password))
    connection = pika.BlockingConnection(params)

    #heroku changes end

    channel = connection.channel()

    #retry queue
    channel.exchange_declare(exchange='worker_exchange',type='fanout')

    queue_name = 'worker_queue'

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
