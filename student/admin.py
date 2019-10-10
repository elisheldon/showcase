from django.contrib import admin

from .models import Student, Item, Link, Gallery, Photo, Document

# Register your models here.
admin.site.register(Student)
admin.site.register(Item)
admin.site.register(Link)
admin.site.register(Gallery)
admin.site.register(Photo)
admin.site.register(Document)