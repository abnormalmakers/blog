from django.conf.urls import url
from .views import Personal_view

urlpatterns=[
    url(r'',Personal_view.as_view(),name='personal')
]