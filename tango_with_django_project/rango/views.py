from django.http import HttpResponse
from django.shortcuts import render
from rango.models import Category,Page
def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {'boldmessage':"These are bold messages from /rango/views.py",
                     'categories':category_list,
                      'pages':page_list  }
    return render(request,'rango/index.html',context_dict)
def about(request):
    context_dict = {'name':'Bin'}
    return render(request,'rango/about.html',context_dict)
def show_category(request, category_name_slug):
    context_dict = {}
    
    try:
        category = Category.objects.get(slug = category_name_slug)
        page = Page.objects.filter(category = category)
        context_dict['pages'] = page
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['pages'] = None
        context_dict['category'] = None
    return render(request, 'rango/category.html',context_dict)

