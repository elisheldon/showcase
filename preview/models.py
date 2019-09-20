from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Create your models here.
class BlacklistUrl(models.Model):
    domain = models.CharField(
        max_length = 128,
    )

    def __str__(self):
        return self.domain