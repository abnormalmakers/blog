var writeblog={
    tag_arr:[],
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
    //发表博客
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
                    'tag':writeblog.tag_arr,
                    'content':$('#blog_content').val()
                },
                success:function(data){
                    console.log(data)
                }
            })
        }else{

        }

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