from django.db import models
from django.conf import settings

# Create your models here.
class Staff(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
    )
    def __str__(self):
        return self.user.username

class School(models.Model):
    name = models.CharField(
        max_length = 128,
    )
    external_id = models.CharField(
        max_length = 16,
        blank = True,
        null = True,
    )
    address = models.CharField(
        max_length = 128,
        blank = True,
        null = True,
    )
    city = models.CharField(
        max_length = 32,
        blank = True,
        null = True,
    )
    state = models.CharField(
        max_length = 32,
        blank = True,
        null = True,
    )
    country = models.CharField(
        max_length = 64,
        blank = True,
        null = True
    )
    zip = models.CharField(
        max_length = 16,
        blank = True,
        null = True,
    )
    code = models.CharField(
        max_length = 6,
        blank = True,
        null = True,
    )
    student_code = models.CharField(
        max_length = 6,
        blank = True,
        null = True,
    )
    owners = models.ManyToManyField(
        Staff,
        related_name = 'schools_owned',
        blank = True,
    )
    staff = models.ManyToManyField(
        Staff,
        related_name = 'schools_staffed',
        blank = True,
    )
    def __str__(self):
        return self.name + ' (' + self.city + ')'