# Generated by Django 2.2.5 on 2019-10-21 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0033_auto_20191018_1129'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='pinned',
            field=models.BooleanField(default=False),
        ),
    ]