from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import pika

@csrf_exempt
def messagePost(request):
    data = json.loads(request.body)
    print "data is",data['message']

    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
    channel = connection.channel()

    #Worker queue
    channel.exchange_declare(exchange='worker_exchange',type='fanout')

    channel.queue_declare(queue='worker_queue')

    channel.queue_bind(exchange='worker_exchange',queue='worker_queue')

    channel.basic_publish(exchange='worker_exchange',
                      routing_key='',
                      body='Hello World!')


    #retry queue
    channel.exchange_declare(exchange='retry_exchange',type='fanout')

    channel.queue_declare(queue='retry_queue',arguments={"x-message-ttl" : 1000, "x-dead-letter-exchange" : "worker_exchange"})

    channel.queue_bind(exchange='retry_exchange',queue='retry_queue')

    connection.close()

    return HttpResponse("Hello, world.")
