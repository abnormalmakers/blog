from django.conf.urls import url
from .views import headers_view

urlpatterns=[
    url(r'^headers/',headers_view)
]