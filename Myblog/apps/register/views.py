from django.shortcuts import render
from main import *
# Create your views here.
def register_views(request):
    if request.method=='GET':
        fn()
    elif request.method=='POST':
        pass
    return render(request,'register.html',locals())