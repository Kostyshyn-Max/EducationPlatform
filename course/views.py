from django.db.models.query import Prefetch
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Lesson, Exercise, Module
from .forms import NewUserForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth import login, authenticate

# Create your views here.
def index(request):
    lessons_list = Lesson.objects.all()
    module_list = Module.objects.all()
    return render(request, 'course/index.html', {'lessons_list': lessons_list, 'module_list': module_list})

def detail(request, lesson_id):
    lesson = Lesson.objects.filter(id = lesson_id)[0]
    return render(request, 'course/detail.html', {'lesson': lesson})

def exercises(request, lesson_id):
    lesson = Lesson.objects.filter(id = lesson_id)[0]
    exercises_list = Exercise.objects.filter(lesson_id = lesson.id)
    return render(request, 'course/exercise/index.html', {'exercises_list': exercises_list, 'lesson': lesson})

def exercise_detail(request, exercise_id):
    exercise = Exercise.objects.filter(id = exercise_id)[0]
    inp_value = request.POST.get('code', '')
    return render(request, 'course/exercise/detail.html', {'exercise': exercise, 'inp_value':inp_value})

def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("/")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request, "course/register.html", {"register_form":form})

def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("/")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="course/login.html", context={"login_form":form})