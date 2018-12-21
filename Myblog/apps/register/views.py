import json
from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse,HttpResponseRedirect
import main
import zhenzismsclient as smsclient
# Create your views here.

class Regster_post():
    def __init__(self,request,apiUrl,appId,appSecret,phone):
        self.request=request
        self.apiUrl=apiUrl
        self.appId = appId
        self.appSecret = appSecret
        self.phone = phone

    # 发送验证码请求
    def valid_code_post(self):
        try:
            client = smsclient.ZhenziSmsClient(self.apiUrl, self.appId, self.appSecret)
            # shengyu = client.balance()
            # print('剩余短信:', shengyu)

            # 随机生成验证码
            valid_code = main.valid_code()
            print(valid_code)

            # 发送验证码并获取返回结果
            result = client.send(self.phone, '您的验证码是%s，请在5分钟内输入'%valid_code)

            # 验证码发送成功 ，将验证码存入session
            result = json.loads(result)
            print('验证码发送code:',result['code'])
            if result['code'] == 0:
                print('存放session')
                self.request.session['valid_code'] = valid_code
                self.request.session.set_expiry(60)
            return json.dumps(result)
        except Exception as e:
            print(e)
            return False

    # 注册请求
    def register_post(self):
        pass






class Register_views(View):
    # 短信验证码参数
    apiUrl = "https://sms_developer.zhenzikj.com"
    appId = 100340
    appSecret = '482bff9b-a65f-451f-89d7-66f7b317dde3'

    def get(self,request):
        valid_code=request.session.get('valid_code',None)
        print("当前验证码valid_code:",valid_code)

        return render(request,'register.html',locals())

    def post(self,request):
        # 判断 是注册请求还是发送验证码
        re_content=request.POST.get('re_content',None)
        # 接受前端注册表单信息
        # 手机号
        phone=request.POST.get('phone',None)
        # 密码
        passw=request.POST.get('password',None)
        # 确认密码
        comfirm_passw=request.POST.get('comfirm_passw',None)
        # 验证码
        msgcode=request.POST.get('msgcode',None)
        # 返回结果
        result=''

        # 后端判断手机号是否合法
        is_valid=main.phoneIsValid(phone)
        if not is_valid:
            dic = {
                'code': 2,
                'msg': '手机号不合法'
            }
            return HttpResponse(json.dumps(dic), content_type='application/json')
        # 判断请求内容
        if re_content=='msg_code':
        #     创建register_post请求对象
            register_post=Regster_post(request,self.apiUrl,self.appId,self.appSecret,phone)
            # 返回短信发送结果
            result=register_post.valid_code_post()
            if not result:
                result={'code':1,'data':'发送失败'}
            return HttpResponse(result, content_type='application/json')
        elif re_content=='user_register':
        #   后端二次验证表单,二次加密

            return HttpResponse('ok',content_type='application/json')
        else:
            dic = {
                'code': 6,
                'msg': '参数传递错误'
            }
            return HttpResponse(json.dumps(dic),content_type='application/json')


