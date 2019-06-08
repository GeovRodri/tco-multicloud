from django.conf.urls import url
from website.views import index
from django.urls import path

urlpatterns = [
    path('', index, name='index'),
]
