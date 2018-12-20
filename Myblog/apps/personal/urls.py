from django.conf.urls import url
from .views import *

urlpatterns=[
    url(r'^personal/',Personal_view.as_view(),name='personal')
]