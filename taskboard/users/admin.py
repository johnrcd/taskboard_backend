from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import TaskboardUser

class TaskboardUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Profile", {"fields": ("name", "title", "about_me")}),
    )

admin.site.register(TaskboardUser, TaskboardUserAdmin)