from django.shortcuts import render

# Create your views here.
def login_views(request):
    if request.method=='GET':
        pass
    elif request.method=='POST':
        pass
    return render(request, 'login.html', locals())