# Generated by Django 2.2.5 on 2019-10-07 19:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0017_auto_20191003_1607'),
    ]

    operations = [
        migrations.AlterField(
            model_name='photo',
            name='image',
            field=models.ImageField(upload_to='images/9d12bcd35c0247ea981d7a76b0511dd2/'),
        ),
    ]