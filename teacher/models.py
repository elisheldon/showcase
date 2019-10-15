from django.db import models
from django.conf import settings

# Create your models here.
class Staff(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
    )

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
        max_length = 8,
        blank = True,
        null = True,
    )
    owners = models.ManyToManyField(
        Staff,
        related_name = 'schools_owned',
    )
    staff = models.ManyToManyField(
        Staff,
        related_name = 'schools_staffed',
    )
    

