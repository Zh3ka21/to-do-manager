from django.urls import path

from tasks.views import base_view_handler

from .views import (
    add_task,
    create_project,
    delete_task,
    edit_task,
    get_tasks_for_date,
    move_task,
    project_dates,
    toggle_task_done,
)

urlpatterns = [
    path('', base_view_handler, name='base_view_handler'),

    path('task/<int:task_id>/toggle/', toggle_task_done, name='toggle_task_done'),
    path('task/<int:task_id>/move/<str:direction>/', move_task, name='move_task'),

    path('add_task/', add_task, name='add_task'),
    path('delete-task/<int:task_id>/', delete_task, name='delete_task'),
    path("task/edit/<int:task_id>/", edit_task, name="edit_task"),

    path('project_dates/', project_dates, name='project_dates'),
    path('create_project/', create_project, name='create_project'),

    path('get_tasks_for_date/', get_tasks_for_date, name='get_tasks_for_date'),
]
