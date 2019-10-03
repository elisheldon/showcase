from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):

    def handle(self, *args, **options):
        if not Group.objects.filter(name='students').exists():
            Group.objects.create(name='students')
        if not Group.objects.filter(name='teachers').exists():
            Group.objects.create(name='teachers')