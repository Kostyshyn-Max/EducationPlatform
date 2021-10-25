from django.shortcuts import render
from django.http import HttpResponse
from .models import Lesson, Exercise

# Create your views here.
def index(request):
    lessons_list = Lesson.objects.all()
    context = {'lessons_list': lessons_list}
    return render(request, 'course/index.html', context)

def detail(request, lesson_id):
    lesson = Lesson.objects.filter(id = lesson_id)[0]
    return render(request, 'course/detail.html', {'lesson': lesson})

def exercises(request, lesson_id):
    lesson = Lesson.objects.filter(id = lesson_id)[0]
    exercises_list = Exercise.objects.filter(lesson_id = lesson.id)
    return render(request, 'course/exercise/index.html', {'exercises_list': exercises_list, 'lesson': lesson})

def exercise_detail(request, exercise_id):
    exercise = Exercise.objects.filter(id = exercise_id)[0]
    return render(request, 'course/exercise/detail.html', {'exercise': exercise})