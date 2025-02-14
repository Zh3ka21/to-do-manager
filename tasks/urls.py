"""Urls router."""
from django.contrib.auth import views as auth_views
from django.urls import path

from tasks.views import base_view_handler

from .views import (
    add_task,
    check_auth_status,
    create_project,
    custom_login,
    custom_logout,
    custom_signup,
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
    path('api/auth-status/', check_auth_status, name='check_auth_status'),

    path('login/', custom_login, name='custom_login'),
    path('signup/', custom_signup, name='custom_signup'),
    path('logout/', custom_logout, name='custom_logout'),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

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
