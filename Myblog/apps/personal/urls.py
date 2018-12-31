from django.conf.urls import url
from .views import Personal_view,Blogdetails_view,WriteBlog_view

urlpatterns=[
    url(r'^$',Personal_view.as_view(),name='personal'),
    url(r'^blogdetails/(\d+)',Blogdetails_view.as_view(),name='blogdetails'),
    url(r'^write/',WriteBlog_view.as_view(),name='writeblog')
]