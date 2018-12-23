var login={
//    表单验证
    checkForm:function(phone,passw){
        $('.login-errmsg').css('display','none').text('')
        if(!phone){
            //手机号为空
            $('.login-errmsg-phone').css('display','block').text('手机号不能为空');
            return false
        }else if(!login.checkPhone(phone)){
            //手机号不存在
            $('.login-errmsg-phone').css('display','block').text('手机号不存在');
            return false
        }else if(!passw){
            //密码为空
            $('.login-errmsg-passw').css('display','block').text('密码不能为空');
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
    },
//    发送登录ajax请求
    loginAjax:function(csrf_token,phone,repassword){
        $.ajax({
            url:'/login/',
            type:'post',
            datatype:'json',
            headers:{"X-CSRFtoken":csrf_token},
            data:{
                'phone':phone,
                'password':repassword
            },
            success:function(data){
                if(data.code==200){
                    console.log('登陆成功')
                    window.location.href='/personal/'
                }else if(data.code==113){
                    $('.login-errmsg-passw').css('display','block').text('密码错误');
                }

            }
        })
    }
}
$(function(){
    //登录页面金庸浏览器回退功能
    if(window.history&&window.history.pushState){
        $(window).on('popstate',function(){
            window.history.pushState('forward',null,'#')
            window.history.forward(1)
        })
    }
    window.history.pushState('forward',null,'#')
    window.history.forward(1)
    $("#login-submit").on('click',function(){
        //获取表单数据
        phone=$('#login-account').val();
        passw=$("#login-password").val();
        //验证表单
        FormIsValid=login.checkForm(phone,passw);
        console.log(FormIsValid);
        if(FormIsValid){
        //    加密密码
            repassword=sha256_digest(passw);
        //    获取csrftoken
            csrf_code=$("#csrftoken").val();
        //    发起登陆请求
            login.loginAjax(csrf_code,phone,repassword)
        }
    })
})