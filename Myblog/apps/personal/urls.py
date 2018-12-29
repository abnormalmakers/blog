from django.conf.urls import url
from .views import Personal_view,Blogdetails_view

urlpatterns=[
    url(r'^$',Personal_view.as_view(),name='personal'),
    url(r'^blogdetails/',Blogdetails_view.as_view(),name='blogdetails')
]