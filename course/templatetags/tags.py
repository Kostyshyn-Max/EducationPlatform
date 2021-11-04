from django import template

register = template.Library()
from io import StringIO
from contextlib import redirect_stdout

@register.simple_tag
def func1(str):
    f = StringIO()
    with redirect_stdout(f):
        exec(str)
    s = f.getvalue()
    return s
