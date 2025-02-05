from django.contrib import admin

from tasks.models import Project, Task

admin.register(Project)
admin.register(Task)
