var alertTip={
    registertips:function(){
        layer.open({
            title:"",
            content:"<div style='text-align:center'>注册成功，正在跳往注册页面</div>",
            closeBtn:0,
            btnAlign:'c',
            time:5000,
            timer:null,
            yes:function(){
                window.location.href='/login/'
            },
            success:function(){
                clearInterval(this.timer);
                this.timer=setInterval(function(){
                    window.location.href='/login/'
                },this.time)
            }
        });
    }
}
