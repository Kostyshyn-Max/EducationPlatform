from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_request, name='register'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('lessons/<int:lesson_id>/', views.detail, name='detail'),
    path('exercises/<int:exercise_id>/', views.exercise_detail, name='exercise_detail')
]