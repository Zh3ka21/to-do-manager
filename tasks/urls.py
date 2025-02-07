from django.urls import path

from tasks.views import base_view_handler

from .views import add_task, delete_task, edit_task, move_task, toggle_task_done

urlpatterns = [
    path('', base_view_handler, name='base_view_handler'),

    path('task/<int:task_id>/toggle/', toggle_task_done, name='toggle_task_done'),
    path('task/<int:task_id>/move/<str:direction>/', move_task, name='move_task'),

    path('add_task/', add_task, name='add_task'),
    path('delete-task/<int:task_id>/', delete_task, name='delete_task'),
    path("task/edit/<int:task_id>/", edit_task, name="edit_task"),
]
