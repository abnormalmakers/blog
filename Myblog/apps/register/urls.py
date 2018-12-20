from django.conf.urls import url
from .views import *

urlpatterns=[
    url(r'^$',register_views,name='register')
]