"""
Configuration for the tasks app.

This module contains the configuration class for the tasks app, including
the definition of the default auto field for models.

Requires:
    Django
"""

from django.apps import AppConfig


class TasksConfig(AppConfig):
    """
    Configuration class for the tasks app.

    Defines app-specific configurations such as the default auto field
    type and the app name.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "tasks"
