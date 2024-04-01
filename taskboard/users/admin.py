from django.contrib import admin
from .models import TaskboardUser

class TaskboardUserAdmin(admin.ModelAdmin):
    pass

admin.site.register(TaskboardUser, TaskboardUserAdmin)