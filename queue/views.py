from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import pika,os,urlparse
from random import randint
import random
import requests

@csrf_exempt
def producemessage(request):
    data = json.loads(request.body)

    '''connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))'''

    #Heroku changes start

    url_str = os.environ.get('CLOUDAMQP_URL', 'amqp://guest:guest@localhost//')
    url = urlparse.urlparse(url_str)
    params = pika.ConnectionParameters(host=url.hostname, virtual_host=url.path[1:],
             credentials=pika.PlainCredentials(url.username, url.password))
    connection = pika.BlockingConnection(params)

    #heroku changes end

    channel = connection.channel()

    #Worker queue
    channel.exchange_declare(exchange='worker_exchange',type='fanout')

    channel.queue_declare(queue='worker_queue')

    channel.queue_bind(exchange='worker_exchange',queue='worker_queue')

    messages = []
    for i in range(10):
        message = {}
        message['url'] = data['callback_url']
        message['msg'] = data['message'] + str(randint(0,100))
        messages.append(message)
        print "pubished message",message

        channel.basic_publish(exchange='worker_exchange',
                          routing_key='worker_queue',
                          body=json.dumps(message))


    #retry queue
    channel.exchange_declare(exchange='retry_exchange',type='fanout')

    channel.queue_declare(queue='retry_queue',arguments={"x-message-ttl" : 1000, "x-dead-letter-exchange" : "worker_exchange"})

    channel.queue_bind(exchange='retry_exchange',queue='retry_queue')

    connection.close()

    return HttpResponse(json.dumps(messages), content_type="application/json")

@csrf_exempt
def callback_service(request):
    print "callback_service is called"
    if random.random() < 0.5:
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=400)
