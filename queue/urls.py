from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^producer/$', views.producemessage, name='producemessage'),
    url(r'^callback_service$', views.callback_service, name='callback_service')
]
