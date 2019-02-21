from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse,HttpResponseRedirect
from django.core.signing import Signer
from .models import Users
import zhenzismsclient as smsclient
import json
import re
import random

# Create your views here.

class Send_msgcode():
    # 初始化验证码发送返回结果
    __result=''

    def __init__(self,request,apiUrl,appId,appSecret,phone):
        self.request=request
        self.apiUrl=apiUrl
        self.appId = appId
        self.appSecret = appSecret
        self.phone = phone

    # 发送验证码请求
    def valid_code_post(self):
        # 验证手机号是否存在
        isRegistered = self.phoneIsRepeat(self.phone)
        if isRegistered:
            # 如果存在，返回失败发送结果
            self.__result = {'code': 103, 'msg': "手机号已存在"}
            return self.__result
        try:
            client = smsclient.ZhenziSmsClient(self.apiUrl, self.appId, self.appSecret)

            # 随机生成验证码
            valid_code = self.generate_valid_code()
            print(valid_code)

            # 发送验证码并获取返回结果
            self.__result = client.send(self.phone, '您的验证码是%s，请在5分钟内输入'%valid_code)

            # 验证码发送成功 ，将验证码存入session
            self.__result = json.loads(self.__result)
            print('验证码发送code:',self.__result['code'])
            if self.__result['code'] == 0:
                self.request.session['valid_code'] = valid_code
                self.request.session.set_expiry(5*60)
            # 返回验证码发送成功结果
            return self.__result
        except Exception as e:
            print(e)
            # 返回验证码发送失败结果
            self.__result={'code':101,'data':'验证码发送失败'}
            return self.__result

    # 随机生成6位数验证码
    @staticmethod
    def generate_valid_code():
        arr = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        s = ''
        for i in range(6):
            s += random.choice(arr)
        return s

    @staticmethod
    def phoneIsRepeat(phone):
        # 判断手机号是否已存在
        isActive = Users.objects.filter(phone=phone)
        if isActive:
            return True
        else:
            return False


class Register_views(View):
    # 短信验证码参数
    __apiUrl = "https://sms_developer.zhenzikj.com"
    __appId = 100340
    __appSecret = '482bff9b-a65f-451f-89d7-66f7b317dde3'
    # 返回结果
    __result=''

    def get(self,request):
        valid_code = request.session.get('valid_code', None)
        print("当前验证码valid_code:", valid_code)
        phone=request.session.get('phone','')
        if phone:
            return HttpResponseRedirect('/personal/?page=1')
        elif request.COOKIES.get('phone',''):
                phone= request.COOKIES.get('phone')
                request.session['phone']=phone
                request.session.set_expiry(60*60*24)
                return HttpResponseRedirect('/personal/?page=1')
        else:
            return render(request, 'register.html', locals())


    def post(self,request):
        # 判断 是注册请求还是发送验证码
        re_content=request.POST.get('re_content',None)
        # 接受前端注册表单信息
        # 手机号
        phone=request.POST.get('phone',None)
        # 密码
        passw=request.POST.get('password',None)
        # 验证码
        msgcode=request.POST.get('msgcode',None)

        #检测手机号是否已存在
        isRegistered=self.phoneIsRepeat(phone)
        if isRegistered:
            dic = {'code': 103, 'msg': "手机号已存在"}
            return HttpResponse(json.dumps(dic), content_type='application/json')

        # 后端二次验证手机号是否合法
        is_valid=self.phoneIsValid(phone)
        if not is_valid:
            dic = {
                'code': 102,
                'msg': '手机号不合法'
            }
            return HttpResponse(json.dumps(dic), content_type='application/json')

        # 判断请求内容
        if re_content=='msg_code':
            #发送验证码请求
            # 创建register_post请求对象
            register_post=Send_msgcode(request,self.__apiUrl,self.__appId,self.__appSecret,phone)
            # 返回短信发送结果
            self.__result=register_post.valid_code_post()
            print(self.__result)
            return HttpResponse(json.dumps(self.__result), content_type='application/json')
        elif re_content=='user_register':
            # 用户注册请求
            # 检测验证码是否正确且未失效
            check_valid_code=request.session.get('valid_code',None)
            if check_valid_code==msgcode:
                # 验证码正确，将用户资料入库
                #后端二次验证表单,密码二次加密
                signer=Signer()
                #二次加密后的密码
                passw_salt=signer.sign(passw)
                #插入数据库
                try:
                    Users.objects.create(phone=phone,password=passw_salt,is_active=True)
                    dic = {'code': 200, 'msg': '插入用户成功'}
                    return HttpResponse(json.dumps(dic), content_type='application/json')
                except Exception as e:
                    dic={'code':108,'msg':'注册用户失败，请重新发送'}
                    return HttpResponse(json.dumps(dic),content_type='application/json')
            else:
                dic = {'code': 106, 'msg': '验证码不正确'}
                return HttpResponse(json.dumps(dic), content_type='application/json')
        else:
            dic = {
                'code': 107,
                'msg': '参数传递错误'
            }
            return HttpResponse(json.dumps(dic),content_type='application/json')

    @staticmethod
    def phoneIsRepeat(phone):
        # 判断手机号是否已存在
        isActive = Users.objects.filter(phone=phone)
        if isActive:
            return True
        else:
            return False

    # 后端手机号验证合法性
    @staticmethod
    def phoneIsValid(tel):
        ret = re.match(r"^1[35678]\d{9}$", tel)
        if ret:
            return True
        else:
            return False


