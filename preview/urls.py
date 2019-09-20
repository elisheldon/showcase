from django.urls import path

from . import views

app_name = 'preview'
urlpatterns = [
    path('', views.index, name='index'),
    path('loadblacklist', views.load_blacklist, name='load_blacklist')
]