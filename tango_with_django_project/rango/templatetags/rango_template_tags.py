from atexit import register
from django import template
from rango.models import Category

register = template.Library()

@register.inclusion_tag('rango/categories.html')
def get_category_inclusion_tag():
    return {'categories': Category.objects.all()}