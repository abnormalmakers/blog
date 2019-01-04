var personal={

};


$(function(){
    //页面跳转
    $('#sure_turnpage').on('click',function(){
        target_page=$('#skip_page').val();
        param_arr=location.search.split('&')
        if(param_arr.length>1){
            window.location.href='/personal/?page='+target_page+'&'+param_arr[1]
        }else{
            window.location.href='/personal/?page='+target_page
        }




    });
});