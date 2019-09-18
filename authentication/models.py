from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class PortfolioUser(AbstractUser):
    pass

    def __str__(self):
        return self.username