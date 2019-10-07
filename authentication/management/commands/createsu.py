from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

import os

#https://realpython.com/deploying-a-django-app-to-aws-elastic-beanstalk/#configuring-a-database

class Command(BaseCommand):

    def handle(self, *args, **options):
        if not get_user_model().objects.filter(username='admin').exists():
            get_user_model().objects.create_superuser('admin', 'kombucha@gmail.com', os.environ['DJANGO_SUPERUSER_PASS'])