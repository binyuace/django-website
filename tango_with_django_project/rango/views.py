from django.http import HttpResponse
from django.shortcuts import render
def index(request):
    context_dict = {'boldmessage':"These are bold messages from /rango/views.py"}
    return render(request,'rango/index.html',context_dict)
def about(request):
    context_dict = {'name':'Bin'}
    return render(request,'rango/about.html',context_dict)
