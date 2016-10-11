from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import pika
from random import randint

@csrf_exempt
def messagePost(request):
    data = json.loads(request.body)

    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
    channel = connection.channel()

    #Worker queue
    channel.exchange_declare(exchange='worker_exchange',type='fanout')

    channel.queue_declare(queue='worker_queue')

    channel.queue_bind(exchange='worker_exchange',queue='worker_queue')

    for i in range(10):
        message = "hello world" + str(randint(0,100))

        print "pubished message",message

        channel.basic_publish(exchange='worker_exchange',
                          routing_key='',
                          body=message)


    #retry queue
    channel.exchange_declare(exchange='retry_exchange',type='fanout')

    channel.queue_declare(queue='retry_queue',arguments={"x-message-ttl" : 1000, "x-dead-letter-exchange" : "worker_exchange"})

    channel.queue_bind(exchange='retry_exchange',queue='retry_queue')

    connection.close()

    return HttpResponse("Hello, world.")
