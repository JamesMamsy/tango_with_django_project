from difflib import context_diff
from unicodedata import category
from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category
from rango.models import Page

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

    return render(request, 'rango/category.html', context=context_dict)