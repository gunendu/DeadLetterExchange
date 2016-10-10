from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def messagePost(request):
    print "view is called"
    print "request data",request.data
    return HttpResponse("Hello, world.")
