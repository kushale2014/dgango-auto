from django import template

register = template.Library()

@register.filter(is_safe=True)
def list_columns(value, column=1):
    for i in range(0, len(value), column):
        yield value[i:i+column]