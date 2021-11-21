from django.db.models.query import Prefetch
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Lesson, Exercise, Module, InputOutputData
from .forms import NewUserForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    form1 = NewUserForm()
    form2 = AuthenticationForm()

    return render(request, 'course/index.html', {'form1': form1, 'form2': form2})


def lessons(request):
    lessons_list = Lesson.objects.all()
    module_list = Module.objects.all()
    return render(request, 'course/lessons.html', {'lessons_list': lessons_list, 'module_list': module_list})


@login_required()
def detail(request, lesson_id):
    if not request.user.is_authenticated:
        redirect('/') 
    lessons_list = Lesson.objects.all()
    current_lesson = lessons_list.filter(id=lesson_id)[0]
    module_list = Module.objects.all()
    exercises_list = Exercise.objects.all()
    return render(request, 'course/detail.html',
                  {'exercises_list': exercises_list, 'lessons_list': lessons_list, 'module_list': module_list,
                   'current_lesson': current_lesson, 'user': request.user})


def exercises(request, lesson_id):
    lesson = Lesson.objects.filter(id=lesson_id)[0]
    exercises_list = Exercise.objects.filter(lesson_id=lesson.id)
    return render(request, 'course/exercise/index.html', {'exercises_list': exercises_list, 'lesson': lesson})

@login_required()
def exercise_detail(request, exercise_id):
    exercise = Exercise.objects.filter(id=exercise_id)[0]
    input_output_list = InputOutputData.objects.filter(exercise=exercise_id)
    inp_value = request.POST.get('code', '')
    lessons_list = Lesson.objects.all()
    module_list = Module.objects.all()
    result_popup_visibility = 'visible' if inp_value != '' else 'hidden'
    return render(request, 'course/exercise/detail.html',
                  {'exercise': exercise, 'inp_value': inp_value, 'lessons_list': lessons_list,
                   'module_list': module_list, 'input_output_list': input_output_list,
                   'result_popup_visibility': result_popup_visibility})


def register_request(request):
    popup = 'hidden'
    form = NewUserForm()
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("/lessons/1")
        messages.error(request, form.errors)
        messages.error(request, "Unsuccessful registration. Invalid information.")
        popup = 'visible'

    return render(request, 'course/index.html', {'form1': form, 'form2': AuthenticationForm(), 'popupR': popup})

def login_request(request):
    popup = 'hidden'
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("/lessons/1")
            else:
                messages.error(request, "Invalid username or password.")
                popup = 'visible'
        else:
            messages.error(request, "Invalid username or password.")
            popup = 'visible'
    return render(request, 'course/index.html', {'form1': NewUserForm(), 'form2': form, 'popupL': popup})
