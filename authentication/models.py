from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class PortfolioUser(AbstractUser):
    email = models.CharField(
        max_length = 256,
    )
    last_name = models.CharField(
        max_length = 150,
        blank = True,
        null = True,
    )

    def __str__(self):
        return self.username