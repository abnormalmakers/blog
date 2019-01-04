var personal={

};


$(function(){
    $('#sure_turnpage').on('click',function(){
        target_page=$('#skip_page').val();
        window.location.href='/personal/?page='+target_page
    })
});