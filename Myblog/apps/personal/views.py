from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse,HttpResponseRedirect
from .models import Article,Article_tag
from register.models import Users
from django.db import transaction
import main
import json
import re
# Create your views here.

# 个人博客页面
class Personal_view(View):
    def get(self,request):
        phone=request.session.get('phone','')
        if phone:
            user=Users.objects.get(phone=phone)
            articles=user.article_set.all().order_by('-article_id')
            return render(request, 'personal.html', locals())
        elif request.COOKIES.get('phone',''):
            phone=request.COOKIES.get('phone','')
            if phone:
                request.session['phone']=phone
                request.session.set_epiry(60*60*24)
                user = Users.objects.get(phone=phone)
                articles = user.article_set.all().order_by('-article_id')
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
            # 找到当前博客
            article=Article.objects.get(article_id=num)
            # 找到当前博客对应的标签
            tags=article.article_tag_set.all().values('tag')
            # 找到作者
            author=article.user
            print(author)
            # 博客内容
            content_arr=article.content.split('\n')

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
            # 判断当前是否处于登录状态
            is_login = main.isLogin(request)
            if is_login:
                title=request.POST.get('title','')
                tag=request.POST.getlist('tag','')
                content = request.POST.get('content', '')
                print(content)
                print(content.split('\n'))
                # 验证博客提交
                if not title:
                    dic={'code':121,'msg':'博客标题不能为空'}
                    return HttpResponse(json.dumps(dic),content_type='application/json')
                elif not content:
                    dic = {'code': 122, 'msg': '博客内容不能为空'}
                    return HttpResponse(json.dumps(dic), content_type='application/json')

                # 查询当前作者id
                user=Users.objects.get(phone=request.session['phone'])
                # 确保数据库的原子操作
                with transaction.atomic():
                    # # 插入博客
                    Article.objects.create(user_id=user.id,title=title,content=content)
                    # 如果选择了文章标签，插入标签
                    # 找到该作者刚刚插入的博客
                    result=Article.objects.filter(user_id=user.id).order_by('-article_id')
                    if tag:
                        for i in tag:
                            # 找到对应的标签，并关联article
                            art_tag=Article_tag.objects.get(tag=i)
                            art_tag.article.add(result[0])

                dic = {'code': 200, 'msg': '发布成功'}
                return HttpResponse(json.dumps(dic), content_type='application/json')

            else:
                return HttpResponseRedirect('/login/')

        except Exception as e:
            print(e)
            dic = {'code': 129, 'msg': '服务器异常'}
            return HttpResponse(json.dumps(dic), content_type='application/json')