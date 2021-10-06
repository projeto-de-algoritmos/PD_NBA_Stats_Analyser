from django import template

import django_tables2

register = template.Library()

@register.simple_tag()
def is_descending(obj):
    if obj is not None:
        if type(obj) == django_tables2.utils.OrderByTuple:
            return obj[0].is_descending
    return False