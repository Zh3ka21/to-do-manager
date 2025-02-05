from django.urls import path

from .views import (
    add_task_to_project,
    create_project_view,
    delete_project_view,
    delete_task_from_project,
    project_detail_view,
    project_list_view,
    update_project_view,
    update_task_in_project,
)

urlpatterns = [
    path("projects/", project_list_view, name="project_list"),
    path("projects/create/", create_project_view, name="create_project"),
    path("projects/<int:project_id>/update/", update_project_view, name="update_project"),
    path("projects/<int:project_id>/delete/", delete_project_view, name="delete_project"),
    path("projects/<int:project_id>/", project_detail_view, name="project_detail"),

    path("projects/<int:project_id>/add_task/", add_task_to_project, name="add_task"),
    path("projects/<int:project_id>/tasks/add/", add_task_to_project, name="add_task"),
    path("projects/<int:project_id>/tasks/<int:task_id>/update/", update_task_in_project, name="update_task"),
    path("projects/<int:project_id>/tasks/<int:task_id>/delete/", delete_task_from_project, name="delete_task"),
]
