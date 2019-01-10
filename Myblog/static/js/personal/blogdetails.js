var blogdetails={
//    删除博客Ajax请求
    del_blog:function(blog_id,csrftoken) {
        $.ajax({
            type: 'post',
            url: '/personal/blogdetails/' + blog_id,
            dataType: 'json',
            headers: {'X-CSRFtoken': csrftoken},
            data: {
                'id': blog_id
            },
            success: function (data) {
                if (data.code == 200) {
                    window.location.href='/personal/?page=1'
                }
            }
        })
    }
};

$(function(){
    $('#del-blog').on('click',function(){
        //博客id
        blog_id=$("#blog_id").val();
        //csrftoken
        csrftoken=$('#csrftoken').val();
        alertTip.confirmTips(blogdetails.del_blog,blog_id,csrftoken);
    })
});