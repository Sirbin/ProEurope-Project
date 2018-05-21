from django.contrib import admin
from user.models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
# Register your models here.


admin.site.register(get_user_model(),UserAdmin)
