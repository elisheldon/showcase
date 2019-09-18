from django.urls import path

from . import views

app_name = 'authentication'
urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('loginUser', views.loginUser, name='loginUser'),
    path('logoutUser', views.logoutUser, name='logoutUser'),
]