from django import template
from datetime import date

register = template.Library()


@register.filter(is_safe=True)
def list_columns(value, column=1):
    for i in range(0, len(value), column):
        yield value[i:i+column]


@register.inclusion_tag('tags/sidebar.html')
def get_sidebar(params):
    return {
        'params': params,
        'prices': [500, 1000, 1200, 1500, 2000] + [i for i in range(3000, 10001, 1000)] + [i for i in range(20000, 50001, 10000)],
        'years': range(date.today().year, 1970-1, -1),
        'counts': [20, 50, 100],
    }


@register.filter
def to_price(value):
    return '{0:,}'.format(value).replace(',', ' ')
