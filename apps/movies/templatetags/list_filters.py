from django import template


register = template.Library()

@register.filter
def timing_movie(value):
    if value < 59:
        return f'{value}м'
    return f'{value // 60}ч {value % 60}м'


@register.filter
def custom_truncatechars(value, arg):
    arg = int(arg)
    if len(value) > arg:
        while value[arg] != ' ' and arg > 0:
            arg -= 1
        if arg <= 0:
            return value
        return value[:arg] + ' ...'
    return value


@register.filter
def translate_content(value):
    content = {'MOVIE': 'ФИЛЬМ', 'SERIAL': 'СЕРИАЛ'}
    return content[value]

