from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from rango.models import Category,Page,UserProfile
from rango.forms import CategoryForm,PageForm,UserForm,UserProfileForm
from django.db import models
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from registration.backends.simple.views import RegistrationView
from rango.websearch import run_query,get_category_list
from django.contrib.auth.models import User

def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    visits = int(request.session.get('visits','1'))
    reset_last_visit_time = False
    last_visit = request.session.get('last_visit')
    if not visits:
        visits = 1
    context_dict = {'boldmessage':"These are bold messages from /rango/views.py",
                     'categories':category_list,
                      'pages':page_list  }

    if last_visit:
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")
        if (datetime.now() - last_visit_time).seconds > 0:
            visits = visits + 1
            reset_last_visit_time = True
    else:
        reset_last_visit_time = True
    if reset_last_visit_time:
        request.session['visits'] = visits
        request.session['last_visit'] = str(datetime.now())
    context_dict['visits'] = visits

    return render(request,'rango/index.html',context_dict)

def about(request):
    context_dict = {'name':'Bin'}
    return render(request,'rango/about.html',context_dict)

def show_category(request, category_name_slug):
    context_dict = {}
    result = []
    if request.method == 'POST':
        query = request.POST['query']
        if query:
            result = run_query(query)

    try:
        category = Category.objects.get(slug = category_name_slug)
        page = Page.objects.filter(category = category).order_by('-views')
        context_dict['pages'] = page
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['pages'] = None
        context_dict['category'] = None
    context_dict['result_list'] = result
    return render(request, 'rango/category.html',context_dict)

def add_category(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            try:
                form.save(commit=True)
                return index(request)
            except models.base.ValidationError:
                print('what?')
        else:
            print(form.errors)
    return render(request, 'rango/add_category.html', {'form':form})

def add_page(request,category_name_slug):
    try:
        category = Category.objects.get(slug = category_name_slug)
    except Category.DoesNotExist:
        category = None
    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            page = form.save(commit=False)
            page.category = category
            page.views = 0
            page.save()
            return show_category(request,category_name_slug)
        else:
            print(form.errors)
    context_dict = {'form':form,'category':category}
    return render(request,'rango/add_page.html',context_dict)

@login_required
def restricted(request):
    return render(request,'rango/restricted.html',{})

class MyRegistrationView(RegistrationView):
    def get_success_url(self,request,user):
        return '/rango/add_profile/'

def search(request):
    result = []
    if request.method == 'POST':
        query = request.POST['query']
        if query:
            result = run_query(query)
    return render(request,'rango/category.html',{'result_list':result})

def track_url(request):
    if request.method == 'GET':
        if 'page_id' in request.GET:
            page_id = request.GET['page_id']
            page = Page.objects.filter( id = int(page_id) )[0]
            if page:
                page.views = page.views + 1
                page.save()
                return HttpResponseRedirect(page.url)
        return HttpResponseRedirect('/rango/')

def register_profile(request):
    if request.method == 'POST':
        profile_form = UserProfileForm(data=request.POST)
        if profile_form.is_valid():
            profile = profile_form.save(commit = False)
            profile.user = request.user
            profile.save()
            return HttpResponseRedirect('/rango/')
        else:
            print(profile_form.errors)
    return render(request,'registration/profile_registration.html',{})

def profile(request):

    context_dict = {'user_profile':UserProfile.objects.get(user = request.user)}
    return render(request,'registration/profile.html',context_dict)
@login_required
def like_category(request):
    likes = 0
    if request.method == 'GET':
        cat = Category.objects.get(id = int(request.GET['category_id']))
        if cat:
            likes = cat.likes + 1
            cat.likes = likes
            cat.save()
    return HttpResponse(likes)
def suggest_category(request):
    cat_list = []
    starts_with = ''
    if request.method == 'GET':
        starts_with = request.GET['suggestion']
        cat_list = get_category_list(8, starts_with)
    return render(request, 'rango/cats.html', {'cats': cat_list })

@login_required
def auto_add_page(request):
    cat_id = None
    url = None
    title = None
    context_dict = {}
    if request.method == 'GET':
        cat_id = request.GET['catid']
        url = request.GET['url']
        title = request.GET['title']
        if cat_id:
            category = Category.objects.get(id=int(cat_id))
            p = Page.objects.get_or_create(category=category, title=title, url=url)
            
            pages = Page.objects.filter(category=category).order_by('-views')
            # Adds our results list to the template context under name pages.
            context_dict['pages'] = pages

    return render(request, 'rango/page_list.html', context_dict)







# def register(request):
#     print('can you print')
#     if request.session.test_cookie_worked():
#         print (">>>> TEST COOKIE WORKED!")
#         request.session.delete_test_cookie()
#     registered = False
#     if request.method == 'POST':
#         user_form = UserForm(data=request.POST)
#         profile_form = UserProfileForm(data=request.POST)
#
#         if user_form.is_valid() and profile_form.is_valid():
#             user = user_form.save()
#             user.set_password(user.password)
#             user.save()
#
#             profile = profile_form.save(commit=False)
#             registered = True
#
#         else:
#             print(user_form.errors,profile_form.errors)
#
#     else:
#         user_form = UserForm()
#         profile_form = UserProfileForm()
#     return render(request,'rango/register.html',
#                     {'user_form':user_form,'profile_form':profile_form,'registered' : registered} )
# def user_login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#
#         user = authenticate(username = username,password = password)
#
#         if user:
#             if user.is_active:
#                 login(request,user)
#                 return HttpResponseRedirect('/rango/')
#             else:
#                 return HttpResponse('Your Rango account is disabled')
#         else:
#             print('Invalid login details:{0}{1}'.format(username,password))
#             return HttpResponse('invalid login details supplied')
#     else:
#         return render(request,'rango/login.html',{})


# @login_required
# def user_logout(request):
#     # Since we know the user is logged in, we can now just log them out.
#     logout(request)
#
#     # Take the user back to the homepage.
#     return HttpResponseRedirect('/rango/')
