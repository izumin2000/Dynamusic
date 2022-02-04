from django import template

register = template.Library()

@register.filter(name='addstr')
def addstr(value, arg):
    """ Only concat string argument """
    if isinstance(arg, str):
        return value + arg
    else:
        return value