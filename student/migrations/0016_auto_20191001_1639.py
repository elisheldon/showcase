# Generated by Django 2.2.5 on 2019-10-01 23:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0015_auto_20191001_1625'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gallery',
            old_name='photo',
            new_name='cover',
        ),
    ]
