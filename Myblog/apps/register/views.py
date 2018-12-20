import json
from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse
# Create your views here.
def register_views(request):
    if request.method=='GET':
        pass
    elif request.method=='POST':
        pass
    return render(request,'register.html',locals())

class Register_views(View):
    def get(self,request):
        return render(request,'register.html',locals())

    def post(self,request):
        print(request.POST)
        print(request.POST['phone'])
        dic={
            'code':200,
            'success':True
        }
        return HttpResponse(json.dumps(dic),content_type='application/json')


