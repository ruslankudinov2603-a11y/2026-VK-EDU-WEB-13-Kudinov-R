from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    extra = 0


class CustomUserAdmin(BaseUserAdmin):
    inlines = [ProfileInline]


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile)
