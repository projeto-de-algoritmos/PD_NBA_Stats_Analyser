from django import template

import django_tables2

register = template.Library()

@register.filter(name='dict_key')
def dict_key(d, k):
    '''Returns the given key from a dictionary.'''
    return d[k]

@register.filter(name="subtract")
def subtract(value, arg):
    return value - arg

@register.simple_tag()
def is_descending(obj):
    if obj is not None:
        if type(obj) == django_tables2.utils.OrderByTuple:
            return obj[0].is_descending
    return False