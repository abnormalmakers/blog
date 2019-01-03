from django.shortcuts import render
from django.views.generic.base import View

# Create your views here.
def headers_view(request):
    return render(request,'header.html',locals())

class Servererror_view(View):
    def get(self,request):
        return render(request,'server_error.html',locals())