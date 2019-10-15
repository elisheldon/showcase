from django.urls import path

from . import views

app_name = 'teacher'
urlpatterns = [
    path('', views.index, name='index'),
    path('schoolSearch', views.schoolSearch, name='schoolSearch'),
    path('loadSchools', views.loadSchools, name='loadSchools'),
]