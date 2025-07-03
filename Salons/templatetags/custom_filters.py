from django import template

register = template.Library()


@register.filter(name='percent')
def percent(value, arg):
    try:
        return int(value) - (int(value) * (int(arg) / 100))
    except TypeError:
        return ''