# Generated by Django 2.2.5 on 2019-10-09 23:55

from django.db import migrations, models
import student.models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0025_auto_20191009_1558'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='file',
            field=models.FileField(upload_to=student.models.get_file_upload_path),
        ),
        migrations.AlterField(
            model_name='photo',
            name='image',
            field=models.ImageField(upload_to=student.models.get_image_upload_path),
        ),
    ]