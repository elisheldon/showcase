# Generated by Django 2.2.5 on 2019-10-15 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0029_auto_20191015_1025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='azure_credentials',
            field=models.CharField(blank=True, max_length=4096, null=True),
        ),
    ]