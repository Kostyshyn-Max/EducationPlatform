from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Lesson)
admin.site.register(Exercise)
admin.site.register(Module)
admin.site.register(InputOutputData)