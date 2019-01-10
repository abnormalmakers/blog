from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse,HttpResponseRedirect
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.db import transaction
from .models import Article,Article_tag
from register.models import Users
import main
import json
import traceback

# Create your views here.

# 个人博客列表页面
class Personal_view(View):
    def get(self,request):
        phone=request.session.get('phone','')
        if phone:
            result_html=self.blog_list(request,phone)
            return result_html

        elif request.COOKIES.get('phone',''):
            phone=request.COOKIES.get('phone','')
            if phone:
                request.session['phone']=phone
                request.session.set_epiry(60*60*24)
                result_html=self.blog_list(request, phone)
                return result_html
        else:
            return HttpResponseRedirect('/login/')



    @staticmethod
    def blog_list(request, phone):
        # 个人博客列表分页
        user = Users.objects.get(phone=phone)
        articles = user.article_set.filter(is_del=False).order_by('-article_id')
        p = Paginator(articles, 5)
        pagenum = request.GET['page']
        tag=request.GET.get('tag','')
        try:
            if tag:
                if tag=='Cadd':
                    tag='C++'
                art_tag=Article_tag.objects.get(tag=tag)

                # 找到该标签对应的博客
                articles_arr=art_tag.article.filter(is_del=False).order_by('-article_id')
                # 从博客结果集中筛选出属于当前用户的博客
                if tag=='C++':
                    art_tag='Cadd'
                articles=[]
                for i in articles_arr:
                    if i.user.id==user.id:
                        articles.append(i)
                # 根据对应的博客构建新的分页对象
                p = Paginator(articles, 5)
                pagenum = request.GET['page']
        except Exception as e:
            traceback.print_exc()
            re = HttpResponseRedirect('/common/servererror')
            return re
        try:
            contacts = p.page(pagenum)
            # 显示多少页 5
            # 总页数小于5页
            if p.num_pages < 5:
                page_range = p.page_range
            else:
                # 当前页码为第一页
                if contacts.number == 1:
                    page_range = range(contacts.number, contacts.number + 5)
                # 当前页码为第二页
                elif contacts.number == 2:
                    page_range = range(contacts.number - 1, contacts.number + 4)
                # 当前页码大于等于第三页   且  当前页码+3小于等于总页数
                elif contacts.number >= 3 and contacts.number + 3 <= p.num_pages:
                    page_range = range(contacts.number - 2, contacts.number + 3)
                # 当前页码+3大于总页数
                elif contacts.number + 3 > p.num_pages:
                    page_range = range(p.num_pages - 4, p.num_pages + 1)
            re = render(request, 'personal.html', locals())
            return re
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            contacts = p.page(1)
            re = render(request, 'personal.html', locals())
            return re
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            contacts = p.page(p.num_pages)
            re = render(request, 'personal.html', locals())
            return re
        except Exception as e:
            traceback.print_exc()
            re = HttpResponseRedirect('/common/servererror')
            return re


#单条博客详情页
class Blogdetails_view(View):
    def get(self,request,num):
        phone=request.session.get('phone','')
        if phone:
            result=self.search_blog(num,phone)
            return render(request,'blogdetails.html',result)
        else:
            if request.COOKIES['phone']:
                request.session['phone']=phone
                request.session.set_epiry(60*60*24)
                result = self.search_blog(num,phone)
                return render(request, 'blogdetails.html', result)
            return HttpResponseRedirect('/login/')

    def post(self,request,num):
        try:
            id=request.POST.get('id','')
            if not id:
                dic = {'code': 204, 'msg': "未找到博客，删除失败"}
                return HttpResponse(json.dumps(dic), content_type="application/json")
            del_blog=Article.objects.get(article_id=id)
            del_blog.is_del=True
            del_blog.save()
            dic={'code':200,'msg':"删除成功"}
            return HttpResponse(json.dumps(dic),content_type="application/json")
        except Exception as e:
            traceback.print_exc()
            dic = {'code': 203, 'msg': "服务器异常,删除失败"}
            return HttpResponse(json.dumps(dic), content_type="application/json")


    @staticmethod
    # 找到对应博客
    def search_blog(num,phone):
        # 找到当前博客
        article = Article.objects.get(article_id=num)
        # 找到当前博客对应的标签
        tags = article.article_tag_set.all().values('tag')
        # 找到作者
        author = article.user
        # 博客内容列表
        content_arr = article.content.split('\n')

        return locals()



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

                # 验证博客提交
                if not title:
                    dic={'code':121,'msg':'博客标题不能为空'}
                    return HttpResponse(json.dumps(dic),content_type='application/json')
                elif not content:
                    dic = {'code': 122, 'msg': '博客内容不能为空'}
                    return HttpResponse(json.dumps(dic), content_type='application/json')

                # 确保数据库的原子操作
                with transaction.atomic():
                    # 查询当前作者id
                    user = Users.objects.get(phone=request.session['phone'])
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
            traceback.print_exc()
            dic = {'code': 129, 'msg': '服务器异常'}
            return HttpResponse(json.dumps(dic), content_type='application/json')