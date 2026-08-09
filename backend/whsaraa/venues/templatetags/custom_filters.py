from django import template

register = template.Library()

@register.filter
def fa_price(value):
    try:
        return '{:,}'.format(int(value))
    except (ValueError, TypeError):
        return value