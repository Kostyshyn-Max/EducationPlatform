from typing import Pattern
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('', RedirectView.as_view(url='lessons/')),
    path('lessons/', include('course.urls')),
    path('admin/', admin.site.urls),
]
