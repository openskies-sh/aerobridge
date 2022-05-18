from django import template

register = template.Library()

@register.filter
def in_(things, category):
    return things.filter(category=category)