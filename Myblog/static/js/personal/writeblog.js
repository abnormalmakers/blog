var writeblog={
    tag_arr:[],
//    页面表单验证
//    1 博客标题为空      2 博客内容为空    3验证成功
    checkForm:function(){
        $(".error_tips").css('display','none');
        title=$('#blog_title').val();
        content=$('#blog_content').val();
        if(!title){
            $(".title_error").css('display','block');
            return 1
        }else if(!content){
            $(".content_error").css('display','block');
            return 2
        }else if(title&&content){
            return 3
        }
    },

//    发布博客ajax请求
    blogpublish_ajax:function(csrftoken,title,content){
        is_valid=writeblog.checkForm();
        if(is_valid==3){
            $.ajax({
                type:'post',
                url:'/personal/write/',
                dateType:"json",
                traditional:true,
                headers:{'X-CSRFtoken':csrftoken},
                data:{
                    'title':title,
                    'tag':writeblog.tag_arr,
                    'content':content
                },
                success:function(data){
                    console.log(data)
                    if(data.code==200){
                        // window.location.href='/personal/'
                        alertTip.errorTips()
                    }else{


                    }
                }
            })
        }
    }

};

$(function(){
    //发表博客
    $("#blog_publish").on('click',function(){
        csrftoken=$('#csrftoken').val();
        title=$('#blog_title').val();
        content=$('#blog_content').val();
        writeblog.blogpublish_ajax(csrftoken,title,content)
    });

//    选择博客标签
    $('.choice_tag').on('change',function(){
        result=writeblog.tag_arr.indexOf(this.value);
        if(result==-1){
             writeblog.tag_arr.push(this.value);
             $('.show_tag').append('<li title="删除">'+this.value+'</li>')
        }else{
            return false
        }
    })

//    删除博客标签
    $(".show_tag").on('click','li',function(){
        index=writeblog.tag_arr.indexOf($(this).html());
        writeblog.tag_arr.splice(index,1);
        $(this).remove();
    })
});