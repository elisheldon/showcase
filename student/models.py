from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.core.files.uploadedfile import InMemoryUploadedFile
from uuid import uuid4
import os
from io import BytesIO
from PIL import Image
from safe_filefield.models import SafeFileField

from teacher.models import Classroom

# Create your models here.
class Student(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    classrooms = models.ManyToManyField(
        Classroom,
        blank = True,
        related_name = 'students'
    )
    age = models.SmallIntegerField(
        default = 0,
    )
    pf_public = models.BooleanField(
        default = False,
    )
    def __str__(self):
        return self.user.username

class Item(models.Model):
    student = models.ForeignKey(
        Student,
        on_delete = models.CASCADE,
    )
    date_time_added = models.DateTimeField(
        auto_now_add = True,
    )
    title = models.CharField(
        max_length = 128,
        blank = True,
    )
    description = models.CharField(
        max_length = 256,
        blank = True,
    )
    sub_item_type = models.ForeignKey(
        ContentType,
        limit_choices_to = models.Q(app_label = 'student', model = 'link') | models.Q(app_label = 'student', model = 'gallery'),
        on_delete = models.CASCADE,
    )
    sub_item_id = models.PositiveIntegerField()
    sub_item = GenericForeignKey('sub_item_type', 'sub_item_id')
    def __str__(self):
        return self.title + ' (' + self.student.user.username + ')'

class Link(models.Model):
    url = models.URLField(
        max_length = 512,
    )
    image = models.CharField(
        max_length = 512,
        blank = True,
        null = True,
    )
    item = GenericRelation(
        Item,
        content_type_field='sub_item_type',
        object_id_field='sub_item_id',
        )
    def __str__(self):
        return self.url + ' (' + self.item.all()[0].student.user.username + ')'

class Gallery(models.Model):
    item = GenericRelation(
        Item,
        content_type_field='sub_item_type',
        object_id_field='sub_item_id',
    )
    cover = models.OneToOneField(
        'Photo',
        on_delete = models.SET_NULL,
        blank = True,
        null = True,
    )

def get_upload_path(instance, filename):
    return os.path.join('images', uuid4().hex, filename)

class Photo(models.Model):
    image = models.ImageField(
        upload_to=get_upload_path
    )
    parent_gallery = models.ForeignKey(
        Gallery,
        on_delete = models.CASCADE,
        related_name = 'photos'
    )

    def save(self, *args, **kwargs):
        if self.image:
            img = Image.open(self.image)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            output = BytesIO()
            img.save(output, format='JPEG', quality=60, optimize=True)
            output.seek(0)
            self.image= InMemoryUploadedFile(output,'ImageField', "%s.jpg" %self.image.name.split('.')[0], 'image/jpeg', output.getbuffer().nbytes, None)
        super(Photo, self).save(*args, **kwargs)

class Document(models.Model):
    file = SafeFileField(
        allowed_extensions=('doc','docx','htm','html','odt','pdf','xls','xlsx','ods','ppt','pptx','txt','pages','numbers','key')
    )
    item = GenericRelation(
        Item,
        content_type_field='sub_item_type',
        object_id_field='sub_item_id',
    )