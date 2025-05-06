from django import template

register = template.Library()

@register.filter(name='multiply')
def multiply(value, arg):
    """İki sayıyı çarpar"""
    try:
        return int(value) * int(arg)
    except (ValueError, TypeError):
        return 0 