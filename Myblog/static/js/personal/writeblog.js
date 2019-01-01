var writeblog={
//    页面表单验证
    checkForm:function(){
        title=$('#blog_title').val();
        content=$('#blog_content').val();
        if(title&&content){
            return true
        }else{
            return false
        }
    }
};

$(function(){
    $("#blog_publish").on('click',function(){
        is_valid=writeblog.checkForm();
        if(is_valid){
            $.ajax({
                type:'post',
                url:'/personal/write/',
                dateType:"json",
                headers:{'X-CSRFtoken':$('#csrftoken').val()},
                data:{
                    'title':$('#blog_title').val(),
                    'content':$('#blog_content').val()
                },
                success:function(data){
                    console.log(data)
                }
            })
        }else{

        }

    })
});