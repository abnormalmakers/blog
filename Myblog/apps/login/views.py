from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse,HttpResponseRedirect
from register.models import Users
from django.core.signing import Signer
import json
# Create your views here.

class Login_view(View):
    # 请求返回结果
    __result=''

    def get(self,request):
        phone=request.session.get('phone','')
        print('login session phone:',phone)
        if phone:
            return HttpResponseRedirect('/personal/?page=1')
        elif request.COOKIES.get('phone',''):
                phone= request.COOKIES.get('phone')
                request.session['phone']=phone
                request.session.set_expiry(60*60*24)
                return HttpResponseRedirect('/personal/?page=1')
        else:
            return render(request, 'login.html', locals())

    def post(self,request):
        phone=request.POST.get('phone',None)
        password=request.POST.get('password',None)
        # 密码二次加盐加密
        signer=Signer()
        pass_salt=signer.sign(password)
        if phone and password:
            try:
                isRegisterPhone=Users.objects.filter(phone=phone)
                if isRegisterPhone:
                    self.__result=Users.objects.filter(phone=phone,password=pass_salt)
                    # 添加session
                    if self.__result:
                        request.session['phone']=phone
                        request.session.set_expiry(60*60*24)
                        dic={'code':200,'msg':'登陆成功'}
                        return HttpResponse(json.dumps(dic),content_type='application/json')
                    else:
                        dic={'code': 113, 'msg': '密码错误'}
                        return HttpResponse(json.dumps(dic), content_type='application/json')
                else:
                    dic = {'code': 112, 'msg': '手机号未注册'}
                    return HttpResponse(json.dumps(dic), content_type='application/json')
            except Exception as e:
                print(e)
                dic={'code':114,'msg':"数据异常"}
                return HttpResponse(json.dumps(dic),content_type='application/json')
        else:
            dic={'code':111,'msg':'手机号或密码不能为空'}
            return HttpResponse(json.dumps(dic),content_type='application/json')

# 退出鞥路
class Logout_view(View):
    def get(self,request):
        response=HttpResponseRedirect('/login/')
        del request.session['phone']
        phone=request.COOKIES.get('phone','')
        if phone:
            response.delete_cookie('phone')
        return response

    def post(self,request):
        pass

