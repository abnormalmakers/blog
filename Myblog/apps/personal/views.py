from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponseRedirect
# Create your views here.


class Personal_view(View):
    def get(self,request):
        phone=request.session.get('phone','')
        if phone:
            return render(request, 'personal.html', locals())
        elif request.COOKIES.get('phone',''):
            phone=request.COOKIES.get('phone','')
            if phone:
                request.session['phone']=phone
                request.session.set_epiry(20)
                return render(request, 'personal.html', locals())
        else:
            return HttpResponseRedirect('/login/')

    def post(self,request):
        pass