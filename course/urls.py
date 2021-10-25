from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:lesson_id>/', views.detail, name='detail'),
    path('<int:lesson_id>/exercises/', views.exercises, name='excercises'),
    path('exercises/<int:exercise_id>/', views.exercise_detail, name='exercise_detail'),
]