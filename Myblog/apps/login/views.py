from django.shortcuts import render
from django.views.generic.base import View
# Create your views here.
# def login_views(request):
#     if request.method=='GET':
#         pass
#     elif request.method=='POST':
#         pass
#     return render(request, 'login.html', locals())


class Login_view(View):
    def get(self,request):
        return render(request, 'login.html', locals())

    def post(self,request):
        pass