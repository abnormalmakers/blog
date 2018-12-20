from django.conf.urls import url
from .views import *

urlpatterns=[
    url(r'^$',login_views,name='login')
]
