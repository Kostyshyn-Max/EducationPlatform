from django import template
from django.utils.html import mark_safe
from io import StringIO
from contextlib import redirect_stdout
from ..models import Lesson, Attempt
from django.contrib.auth import login, authenticate
import sys
import re
from datetime import datetime

register = template.Library()


@register.simple_tag
def func1(str, input_output_list, exercise, user):
    sp = []
    code = ''
    for i in range(len(input_output_list)):
        sys.stdin = StringIO(input_output_list[i].input)
        f = StringIO()
        with redirect_stdout(f):
            try:
                exec(str)
                code = str
            except Exception as e:
                return e
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
            if code != "":
                attempt = Attempt.objects.create(
                    exercise=exercise, code=code, pub_date=datetime.now(), result=False, user=user)
            result = f'Failed at test {i + 1}, your code output { output[i]}'
            return result
    if code != "":
        attempt = Attempt.objects.create(
            exercise=exercise, code=code, pub_date=datetime.now(), result=True, user=user)

    result = 'Conrgatulations!!! All tests are done'
    return result


@register.simple_tag
def is_completed(user, exercise):
    return "completed" if len(Attempt.objects.filter(user=user, exercise_id=exercise.id, result=1)) != 0 else ""


@register.simple_tag
def if_current(lesson1ID, lesson2ID, str):
    return mark_safe(str if lesson1ID == lesson2ID else "")


@register.simple_tag
def is_lesson_completed(lesson, user):
    if lesson.exercises.all().count() == 0:
        return ""

    for exercise in lesson.exercises.all():
        if is_completed(user, exercise) == "":
            return ""

    return "completed"


@register.simple_tag
def is_module_completed(module, user):
    if module.lessons.all().count() == 0:
        return ""

    for lesson in module.lessons.all():
        if is_lesson_completed(lesson, user) == "":
            return ""

    return "completed"


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


@register.simple_tag
def int_to_Roman(num):
    if num != 1:
        num -= 4
    val = [
        1000, 900, 500, 400,
        100, 90, 50, 40,
        10, 9, 5, 4,
        1
    ]
    syb = [
        "M", "CM", "D", "CD",
        "C", "XC", "L", "XL",
        "X", "IX", "V", "IV",
        "I"
    ]
    roman_num = ''
    i = 0
    while num > 0:
        for _ in range(num // val[i]):
            roman_num += syb[i]
            num -= val[i]
        i += 1
    return roman_num


@register.simple_tag
def first_lesson_id(module_id):
    return Lesson.objects.filter(module__id=module_id)[0].id
