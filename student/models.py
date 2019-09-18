from django.db import models
from django.contrib.auth.models import User

from teacher.models import Classroom

# Create your models here.
class Student(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    classrooms = models.ManyToManyField(
        Classroom,
        blank = True,
        related_name = 'students'
    )

class Item(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete = models.CASCADE,
    )
    dateTimeAdded = models.DateTimeField(
        auto_now_add = True,
    )
    url = models.URLField(
        max_length = 512,
    )
    title = models.CharField(
        max_length = 256,
        blank = True,
    )
    description = models.TextField(
        max_length = 1024,
        blank = True,
    )

