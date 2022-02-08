from difflib import context_diff
from unicodedata import category
from urllib import request
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm

def index(request):

    #Returns a list of a query of the top 5 categories by likes
    category_list = Category.objects.order_by('-likes')[:5]
    pages_list = Page.objects.order_by('-views')[:5]

    #Dict for template engine, boldmessage is like a variable for use in the html\
    #Added the category list as it's own dict entry 
    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    context_dict['pages'] = pages_list
    #2nd param is tempalte we want to use
    return render(request, 'rango/index.html', context=context_dict)

def about(request):

    #Contect Dict will store author name here
    context_dict = {'authorName' : 'James Miller'}

    return render(request, 'rango/about.html', context = context_dict)

def show_category(request, category_name_slug):
    context_dict = {}
    try:    
        #Find the category based off the provided slug
        category = Category.objects.get(slug=category_name_slug)

        #Find all pages based in that category, pass them to our context dict
        pages = Page.objects.filter(category=category)

        #Pass the returned values onto our render function
        context_dict['pages'] = pages
        context_dict['category'] = category

    except Category.DoesNotExist:

        #If we cant find one, set to none
        context_dict['category'] = None
        context_dict['pages'] = None

    return render(request, 'rango/category.html/', context=context_dict)

@login_required
def add_category(request):
    form = CategoryForm()

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():

            form.save(commit=True)

            return redirect('/rango/')

        else:
            print(form.errors)
    
    return render(request, 'rango/add_category.html', {'form': form})

@login_required
def add_page(request, category_name_slug):
    try: 
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category=None

    if category is None:
        return redirect('/rango/')

    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()

            return redirect(
                reverse('rango:show_category', 
                kwargs={'category_name_slug': category_name_slug}
                ))
        else:
            print(form.errors)

    context_dict = {'form':form, 'category':category}
    return render(request, 'rango/add_page.html', context=context_dict)

def register(request):
    registered = False

    if request.method == 'POST':

        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            registered = True

        else:
            print(user_form.errors, profile_form.errors)
    
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'rango/register.html', 
    context = {'user_form':user_form,
                'profile_form': profile_form,
                'registered': registered})

def user_login(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:

            if user.is_active:
                login(request, user)
                return redirect(reverse('rango:index'))
            else:
                return HttpResponse("Your Rango account is disabled")

        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied")
    else:
        return render(request, 'rango/login.html')

def user_logout(request):
    logout(request)
    return redirect(reverse('rango:index'))

@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')

