from django.urls import path, re_path, reverse_lazy
from django.contrib.auth import views as auth_views

from . import views

app_name = 'authentication'
urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('loginUser', views.loginUser, name='loginUser'),
    path('logoutUser', views.logoutUser, name='logoutUser'),
    path('privacy', views.privacy, name='privacy'),
    re_path(r'^password_reset/$', auth_views.PasswordResetView.as_view(success_url=reverse_lazy('authentication:password_reset_done')), name='password_reset'),
    re_path(r'^password_reset/done/$', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    re_path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.PasswordResetConfirmView.as_view(success_url=reverse_lazy('authentication:password_reset_complete')), name='password_reset_confirm'),
    re_path(r'^reset/done/$', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]