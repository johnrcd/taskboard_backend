from django.contrib import admin
from .models import Project, Task, Comment


class ProjectAdmin(admin.ModelAdmin):
    pass


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0 # the default of 3 sucks lol

    def has_change_permission(self, request, obj):
        return False


class TaskAdmin(admin.ModelAdmin):
    inlines = [CommentInline,] # do not use a string here, it will break
    pass


admin.site.register(Project, ProjectAdmin)
admin.site.register(Task, TaskAdmin)