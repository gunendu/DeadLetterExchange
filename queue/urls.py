from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^producer/$', views.producemessage, name='producemessage'),
    url(r'^consumer/$', views.consumemessage, name='consumemessage'),
]
