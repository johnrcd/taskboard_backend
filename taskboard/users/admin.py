from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import TaskboardUser

class TaskboardUserAdmin(UserAdmin):
    pass

admin.site.register(TaskboardUser, TaskboardUserAdmin)