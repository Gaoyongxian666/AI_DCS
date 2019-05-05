from django.contrib import admin

# Register your models here.

# 因为同一个目录，所以可以直接.models
from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserProfile,UserProfileAdmin)

