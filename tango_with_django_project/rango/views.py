from difflib import context_diff
from django.shortcuts import render
from django.http import HttpResponse

def index(request):

    #Dict for template engine, boldmessage is like a variable for use in the html
    context_dict = {'boldmessage' : 'Crunchy, creamy, cookie, candy, cupcake!'}

    #2nd param is tempalte we want to use
    return render(request, 'rango/index.html', context=context_dict)

def about(request):

    #Contect Dict will store author name here
    context_dict = {'authorName' : 'James Miller'}

    return render(request, 'rango/about.html', context = context_dict)
