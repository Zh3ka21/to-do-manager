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
    soft_delete_project,
    toggle_task_done,
    update_project_name,
)

urlpatterns = [
    path("", base_view_handler, name="base_view_handler"),

    path("add_task/", add_task, name="add_task"),
    path("delete_task/<int:task_id>/", delete_task, name="delete_task"),
    path("task/edit/<int:task_id>/", edit_task, name="edit_task"),
    path("move_task/<int:taskId>/<str:direction>/", move_task, name="move_task"),
    path("task/<int:task_id>/toggle/", toggle_task_done, name="toggle_task_done"),

    path("project_dates/", project_dates, name="project_dates"),
    path("create_project/", create_project, name="create_project"),
    path("get_tasks_for_date/", get_tasks_for_date, name="get_tasks_for_date"),

    path("update_project_name/<int:project_id>/", update_project_name, name="update_project_name"),
    path("soft_delete_project/<int:project_id>/", soft_delete_project, name="soft_delete_project"),
]
