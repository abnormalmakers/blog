from django.conf.urls import url
from .views import headers_view,Servererror_view

urlpatterns=[
    url(r'^headers/',headers_view),
    url(r'^servererror/',Servererror_view.as_view(),name='servererror')
]