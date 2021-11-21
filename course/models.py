from django.db import models
from django.db.models.deletion import CASCADE
from django.contrib.auth import get_user_model

# Create your models here.
class Module(models.Model):
    name = models.CharField(max_length=255)

class Lesson(models.Model): 
    name = models.CharField(max_length=255)
    theory = models.TextField()
    module = models.ForeignKey(Module, related_name="lessons", on_delete=models.CASCADE)

class LessonUser(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    lessons = models.ManyToManyField(Lesson)

class Exercise(models.Model):
    name = models.CharField(max_length=255)
    condition = models.TextField()
    sample_input = models.TextField()
    sample_output = models.TextField()
    lesson = models.ForeignKey(Lesson, related_name="exercises", on_delete=models.CASCADE)

class InputOutputData(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    input = models.TextField()
    output = models.TextField()

class Attempt(models.Model):
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    code = models.TextField()
    pub_date = models.DateTimeField()
    result = models.BooleanField() 