var register={
    //初始化验证码计时器
    timer:null,
    //初始化验证码倒计时时间
    countdown:10,
    // 检测注册表单是否填写完整,手机号是否合法
    // 参数为表单信息
    // 返回布尔值
    checkForm:function(phone,passw,confirmpassw,msgcode){
        $('.register-errmsg').css('display','none')
        if(!phone){
            $('.register-errmsg-phone').css('display','block').text('手机号不能为空');
            return false
        }else if(!this.checkPhone(phone)){
            $('.register-errmsg-phone').css('display','block').text('手机号不存在');
            return false
        }else if(!passw){
            $('.register-errmsg-passw').css('display','block');
            return false
        }else if(!confirmpassw){
            $('.register-errmsg-surepassw').css('display','block');
            return false
        }else if(!msgcode){
            $('.register-errmsg-msgcode').css('display','block');
            return false
        }else{
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
        if(register.countdown!=0 && register.countdown!=10){
            return false
        }
        //向后端发送手机号


        //重新初始化计时数
        register.countdown=10;

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
        //验证表单是否有效
        FormisValide=register.checkForm(rephone,repassword,reconfirmpassword,remsgcode);
        console.log(FormisValide)

        //向后台发起ajax请求
        $.ajax({
            url:'/register/',
            type:'post',
            dataType:'json',
            headers:{ "X-CSRFtoken":$('#csrftoken').val()},
            data:{
                'phone':$('#register-phone').val()
            },
            success:function(data){
                console.log(data,typeof(data))
                console.log(data.code)
            }
        })
    });


});


