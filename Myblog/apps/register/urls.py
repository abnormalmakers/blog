from django.conf.urls import url
from .views import *

urlpatterns=[
    url(r'^$',Register_views.as_view(),name='register')
]