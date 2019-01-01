from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse,HttpResponseRedirect
import json
# Create your views here.

# 个人博客页面
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

#单条博客详情页
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



# 写博客
class WriteBlog_view(View):
    def get(self,request):
        phone = request.session.get('phone', '')
        if phone:
            return render(request, 'writeblog.html', locals())
        else:
            phone=request.COOKIES.get('phone','')
            if phone:
                request.session['phone'] = phone
                request.session.set_epiry(60 * 60 * 24)
                return render(request, 'writeblog.html', locals())
            else:
                return HttpResponseRedirect('/login/')

    def post(self,request):
        try:
            title=request.POST.get('title','')
            content = request.POST.get('content', '')
            # 验证博客提交
            if not title:
                dic={'code':121,'msg':'博客标题不能为空'}
                return HttpResponse(json.dumps(dic),content_type='application/json')
            elif not content:
                dic = {'code': 122, 'msg': '博客内容不能为空'}
                return HttpResponse(json.dumps(dic), content_type='application/json')

        except Exception as e:
            print(e)
            dic = {'code': 129, 'msg': '服务器异常'}
            return HttpResponse(json.dumps(dic), content_type='application/json')