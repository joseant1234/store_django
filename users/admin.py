from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin

# se registrar la nueva clase user en el site
admin.site.register(User, UserAdmin)
