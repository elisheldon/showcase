# Generated by Django 2.2.5 on 2019-10-08 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0021_auto_20191008_1442'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='image',
            field=models.ImageField(upload_to='images/666d0c555ab042bba6f273d03690cf9a/'),
        ),
    ]