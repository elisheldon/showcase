from django.urls import path

from . import views

app_name = 'teacher'
urlpatterns = [
    path('', views.index, name='index'),
    path('schoolSearch', views.schoolSearch, name='schoolSearch'),
    path('loadSchools', views.loadSchools, name='loadSchools'),
    path('addSchool', views.addSchool, name='addSchool'),
    path('schoolDetails/<int:id>', views.schoolDetails, name='schoolDetails'),
    path('createSchoolCode', views.createSchoolCode, name='createSchoolCode'),
    path('settings', views.settings, name='settings'),
]