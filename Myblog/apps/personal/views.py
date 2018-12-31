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
                request.session.set_epiry(60*60*24)
                return render(request, 'personal.html', locals())
        else:
            return HttpResponseRedirect('/login/')

    def post(self,request):
        pass


class Blogdetails_view(View):
    def get(self,request,num):
        phone=request.session.get('phone','')
        if phone:
            return render(request,'blogdetails.html',locals())
        else:
            if request.COOKIES['phone']:
                request.session['phone']=phone
                request.session.set_epiry(60*60*24)
                return render(request, 'blogdetails.html', locals())
            return HttpResponseRedirect('/login/')

    def post(self,request):
        pass




class WriteBlog_view(View):
    def get(self,request):
        phone = request.session.get('phone', '')
        if phone:
            return render(request, 'writeblog.html', locals())
        else:
            if request.COOKIES['phone']:
                request.session['phone'] = phone
                request.session.set_epiry(60 * 60 * 24)
                return render(request, 'writeblog.html', locals())
            return HttpResponseRedirect('/write/')