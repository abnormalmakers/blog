var register={
    //初始化验证码计时器
    timer:null,
    //初始化验证码倒计时时间
    countdown:60,
    // 检测注册表单是否填写完整,手机号是否合法
    // 参数为表单信息
    // 返回布尔值
    checkForm:function(phone,passw,confirmpassw,msgcode){
        console.log(passw.length)
        $('.register-errmsg').css('display','none')
        if(!phone){
            //手机号为空
            $('.register-errmsg-phone').css('display','block').text('手机号不能为空');
            return false
        }else if(!this.checkPhone(phone)){
            //手机号不存在
            $('.register-errmsg-phone').css('display','block').text('手机号不存在');
            return false
        }else if(!passw){
            //密码为空
            $('.register-errmsg-passw').css('display','block').text('密码不能为空');
            return false
        }else if(6>passw.length || passw.length>11){
        //    密码长度为6-11
            $('.register-errmsg-passw').css('display','block').text('密码长度为6-11位')
        }else if(!confirmpassw){
            //确认密码为空
            $('.register-errmsg-surepassw').css('display','block').text('确认密码不能为空');
            return false
        }else if(confirmpassw!=passw){
            //密码输入不一致
            $('.register-errmsg-surepassw').css('display','block').text('密码输入不一致');
            return false
        }else if(!msgcode){
            //验证码输入不正确
            $('.register-errmsg-msgcode').css('display','block');
            return false
        }else{
            //表单验证成功
            return true
        }
    },
    //判断手号是否合法
    //参数：手机号码
    //返回值：布尔
    checkPhone:function(phone) {
        if(!phone){
            return false
        }
        var myreg=/^[1][3,4,5,7,8][0-9]{9}$/;
        if(!myreg.test(phone)) {
            return false;
        } else {
            return true;
        }
    },
//   发送验证码ajax
    msgcodeAjax:function(csrf_token,re_content,phone){
        //向后台发起ajax请求
        $.ajax({
            url:'/register/',
            type:'post',
            dataType:'json',
            headers:{ "X-CSRFtoken":csrf_token},
            data:{
                're_content':re_content,
                'phone':phone
            },
            success:function(data){
                console.log(data)
                if(data.code==0){
                    console.log('短信发送成功')
                }else{
                    console.log("短信发送失败")
                }
            }
        })
    }
};

$(function(){
//发送验证码点击事件
    $("#register-sendmessage").on('click',function(){
        //保存发送验证码按钮对象
        that=$(this);

        // 验证手机号是否存在且有效
        rephone=$('#register-phone').val();
        phoneIsValid=register.checkPhone(rephone);

        //没通过验证
        if(!phoneIsValid){
            $('.register-errmsg-phone').css('display','block').text('手机号不合法');
            return false
        }else{
            $('.register-errmsg-phone').css('display','none');
        }
        
        //打开验证码遮罩
        $('#register-sendemail-model').css('display','block');

        //防止前端手动去掉遮罩导致短信重发
        if(register.countdown!=0 && register.countdown!=60){
            return false
        }
        //向后端发送 经过验证后的手机号
        csrf_code=$('#csrftoken').val();
        register.msgcodeAjax(csrf_code,'msg_code',rephone);

        //重新初始化计时数
        register.countdown=60;

        //清除定时器
        clearInterval(register.timer);
        //开启倒计时计时器
        register.timer=setInterval(function(){
            //验证码倒计时秒数
            that.text(register.countdown+' 秒');
            //判断是否超时
            if(register.countdown>0){
                register.countdown--;
            }else{
                clearInterval(register.timer);
                that.text('重新发送');
                //关闭遮罩
                $('#register-sendemail-model').css({
                    'display':'none'
                });
            }
        },1000)
    });


//点击按钮注册
    $('#register-submit').on('click',function(){
        //手机号
        rephone=$('#register-phone').val();
        //手机密码
        repassword=$('#register-password').val();
        ////确认密码
        reconfirmpassword=$("#register-confirmpassword").val();
        //验证码
        remsgcode=$('#register-msgcode').val();
        //验证表单是否有效，返回布尔值
        FormisValide=register.checkForm(rephone,repassword,reconfirmpassword,remsgcode);
        console.log(FormisValide)

        //获取csrftoken码
        csrf_code=$('#csrftoken').val();

        if(FormisValide){
        //    加密密码
            repassword=sha256_digest(repassword)
            console.log(repassword)
        //    表单有效，向后端发起ajax请求
            $.ajax({
                url:'/register/',
                type:'post',
                dataType:'json',
                headers:{"X-CSRFtoken":csrf_code},
                data:{
                    're_content':'user_register',
                    'phone':rephone,
                    'password':repassword,
                    'msgcode':remsgcode
                },
                success:function(data){
                    console.log(data)
                }
            })
        }
    });


});


