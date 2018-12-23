from django.shortcuts import render

# Create your views here.
def headers_view(request):
    return render(request,'header.html',locals())