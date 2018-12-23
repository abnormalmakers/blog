from django.conf.urls import url
from .views import *

urlpatterns=[
    url(r'^$',Login_view.as_view(),name='login'),
    url(r'^logout/',Logout_view.as_view())
]
