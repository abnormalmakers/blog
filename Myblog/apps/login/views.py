from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse
from register.models import Users
from django.core.signing import Signer
import json
# Create your views here.

class Login_view(View):
    # 请求返回结果
    __result=''

    def get(self,request):
        return render(request, 'login.html', locals())

    def post(self,request):
        phone=request.POST.get('phone',None)
        password=request.POST.get('password',None)
        # 密码二次加盐加密
        signer=Signer()
        pass_salt=signer.sign()
        if phone and password:
            try:
                self.__result=Users.objects.filter(phone=phone,password=pass_salt)
                # 添加session
                request.session['phone']=phone
                request.session.set_expiry(60*60*24)
                dic={'code':200,'msg':'登陆成功'}
                return HttpResponse(json.dumps(dic),content_type='application/json')
            except Exception as e:
                print(e)
                dic={'code':114,'msg':"数据异常"}
                return HttpResponse(json.dumps(dic),content_type='application/json')
        else:
            dic={'code':111,'msg':'手机号或密码不能为空'}
            return HttpResponse(json.dumps(dic),content_type='application/json')

