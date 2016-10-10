from django.conf.urls import *

from django.contrib import admin

urlpatterns = [
    url(r'^queue/', include('queue.urls')),
]
