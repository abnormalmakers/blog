from django.shortcuts import render
from django.views.generic.base import View
# Create your views here.


class Personal_view(View):
    def get(self,request):
        return render(request,'personal.html',locals())

    def post(self,request):
        pass