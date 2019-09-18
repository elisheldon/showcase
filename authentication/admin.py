from django.contrib import admin
from django.contrib.auth.admin import UserAdmin 

from .models import PortfolioUser

admin.site.register(PortfolioUser, UserAdmin)