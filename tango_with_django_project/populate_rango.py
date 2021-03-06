import os
from unicodedata import category
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')

import django
django.setup()

from rango.models import Category, Page

def populate():

    #Dict of pages to add into each category
    #Python Category
    python_pages = [
        {'title': 'Official Python Tutorial', 'url':'http://docs.python.org/3/tutorial/', 'views' : 156},
        {'title':'How to Think like a Computer Scientist','url':'http://www.greenteapress.com/thinkpython/', 'views': 2},
        {'title':'Learn Python in 10 Minutes','url':'http://www.korokithakis.net/tutorials/python/', 'views': 365 },
    ]

    #Django Category
    django_pages = [
        {'title': 'Official Django Tutorial', 'url':'https://docs.djangoproject.com/en/2.1/intro/tutorial01/', 'views': 420},
        {'title': 'Django Rocks', 'url':'https://www.djangorocks.com/', 'views': 113},
        {'title': 'How to Tango with Django', 'url':'https://www.tangowithdjango.com/', 'views': 1}        
    ]

    #Other Category
    other_pages = [
        {'title':'Bottle', 'url':'http://bottlepy.org/docs/dev', 'views': 30},
        {'title':'Flask', 'url':'http://flask.pocoo.org', 'views': 42},
    ]

    #Dictionary of Categories to pages
    cats = {
        'Python': {'pages': python_pages, 'views':128, 'likes':64},
        'Django':{'pages': django_pages, 'views':64, 'likes':32},
        'Other Frameworks' : {'pages': other_pages, 'views': 32, 'likes':16}
    }

    #Change above dictionaries to populate with more categories (make sure to add it into the cats category)

    #For each category, add the category
    #then for each page in the category data 
    #add the page with its title and url
    for cat, cat_data in cats.items():
        c = add_cat(cat, cat_data['views'], cat_data['likes'])
        for p in cat_data['pages']:
            add_page(c,p['title'],p['url'])

    #For each category c
    #For each page in category c
    #Print -Category : Page
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print(f'- {c}: {p}')

def add_page(cat, title, url, views=0,):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url = url
    p.views=views
    p.save()

    return p

def add_cat(name, views, likes):
    c = Category.objects.get_or_create(name=name)[0]
    c.views = views
    c.likes = likes
    c.save()
    return c


if __name__ == '__main__':
    print('Starting Rango population script...')
    populate()