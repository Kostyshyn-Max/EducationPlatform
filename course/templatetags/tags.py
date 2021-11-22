from django import template
from django.utils.html import mark_safe
from io import StringIO
from contextlib import redirect_stdout
from django.contrib.auth import login, authenticate
import sys
import re

register = template.Library()

@register.simple_tag
def func1(str, input_output_list):
    sp = []

    for i in range(len(input_output_list)):
        sys.stdin = StringIO(input_output_list[i].input)
        f = StringIO()
        with redirect_stdout(f):
            exec(str)
        s = f.getvalue()
        sp.append(s)
        
    new_sp = []
    output = []
    for i in range(len(input_output_list)):
        output.append(input_output_list[i].output)
    for string in sp:
        new_element = re.sub(r'[ \t]+', ' ', string)
        new_element = re.sub(r'[ \t]*[\n\r]+[ \t]*', '\r\n', new_element)
        new_element = re.sub(r'[ \t]*[\n\r]+[ \t]*$', '', new_element)
        new_element = re.sub(r'^[ \t]*[\n\r]+[ \t]*', '', new_element)
        new_sp.append(new_element)
    result = ''
    for i in range(len(new_sp)):
        if output[i] != new_sp[i]:
           result = f'Failed at test {i + 1}'
           return result
    result = 'Conrgatulations!!! all test are done'
    return result

@register.simple_tag
def if_current(lesson1ID, lesson2ID, str):
    return mark_safe(str if lesson1ID == lesson2ID else "")

@register.filter(name='add_classes')
def add_classes(value, arg):
    css_classes = value.field.widget.attrs.get('class', '')
    if css_classes:
        css_classes = css_classes.split(' ')
    else:
        css_classes = []
    args = arg.split(' ')
    for a in args:
        if a not in css_classes:
            css_classes.append(a)
    return value.as_widget(attrs={'class': ' '.join(css_classes)})