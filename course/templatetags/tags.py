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
    program_code_output = []
    code = ''
    for i in range(len(input_output_list)):
        # last_symbol_code = ord(input_output_list[0].input[
        #    input_output_list[0].input.find('\n') - 1])
        new_input = input_output_list[i].input.replace('\r', '')
        sys.stdin = StringIO(new_input)
        f = StringIO()
        with redirect_stdout(f):
            try:
                exec(str)
                code = str
            except Exception as e:
                return e
        s = f.getvalue()
        program_code_output.append(s)

    good_program_code_output = []
    expected_output = []
    for i in range(len(input_output_list)):
        expected_output.append(input_output_list[i].output)
    for string in program_code_output:
        new_element = re.sub(r'[ \t]+', ' ', string)
        new_element = re.sub(r'[ \t]*[\n\r]+[ \t]*', '\r\n', new_element)
        new_element = re.sub(r'[ \t]*[\n\r]+[ \t]*$', '', new_element)
        new_element = re.sub(r'^[ \t]*[\n\r]+[ \t]*', '', new_element)
        good_program_code_output.append(new_element)
    result = ''
    for i in range(len(good_program_code_output)):
        if expected_output[i] != good_program_code_output[i]:
            if code != "":
                attempt = Attempt.objects.create(
                    exercise=exercise, code=code, pub_date=datetime.now(), result=False, user=user)
            result = f'Failed at test {i + 1}, your code output {good_program_code_output[i]}'
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
