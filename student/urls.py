from django.urls import path

from . import views

app_name = 'student'
urlpatterns = [
    path('', views.portfolio, name='portfolio'),
    path('add', views.add, name='add'),
    path('remove', views.remove, name='remove'),
    path('gallery/<int:item_id>', views.gallery, name='gallery'),
]

