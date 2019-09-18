from django.db import models
from django.conf import settings

# Create your models here.
class Teacher(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
    )

class Classroom(models.Model):
    teacher = models.ForeignKey(
        Teacher,
        on_delete = models.SET_NULL,
        null = True,
    )
    name = models.CharField(
        max_length = 64,
    )

