# Generated by Django 2.2.5 on 2019-10-03 23:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0016_auto_20191001_1639'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='image',
            field=models.ImageField(upload_to='images/b917d241626843909d220b5fb86ffafa/'),
        ),
    ]