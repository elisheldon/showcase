# Generated by Django 2.2.5 on 2019-10-09 22:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0024_student_pf_public'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='')),
            ],
        ),
        migrations.AlterField(
            model_name='link',
            name='image',
            field=models.CharField(blank=True, max_length=512, null=True),
        ),
    ]
