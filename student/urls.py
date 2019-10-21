from django.urls import path

from . import views

app_name = 'student'
urlpatterns = [
    path('', views.portfolio, name='portfolio'),
    path('add', views.add, name='add'),
    path('remove', views.remove, name='remove'),
    path('gallery/<int:item_id>', views.gallery, name='gallery'),
    path('public', views.public, name='public'),
    path('view/<str:username>', views.view, name='view'),
    path('get_google_scopes', views.get_google_scopes, name='get_google_scopes'),
    path('settings', views.settings, name='settings'),
    path('pin', views.pin, name='pin'),
]

