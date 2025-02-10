"""
Tests for creating projects and tasks in the tasks app.

These tests validate the creation of Project and Task objects, ensuring that
attributes such as the project name, user, and task details are set correctly.

Requires:
    pytest
    Django
"""

from datetime import datetime

import pytest
from django.contrib.auth import get_user_model

from tasks.models import Project, Task

# Get the User model from Django
User = get_user_model()


@pytest.mark.django_db
def test_create_project() -> None:
    """
    Test the creation of a Project object.

    Validates that a project is created with the correct attributes, including
    the project name and associated user.
    """
    user = User.objects.create_user(username="testuser", password="testpass")
    project = Project.objects.create(user=user, name="Test Project", project_date="2025-02-10")

    # Assertions to ensure the project is correctly created
    assert project.name == "Test Project"
    assert project.user == user


@pytest.mark.django_db
def test_create_task() -> None:
    """
    Test the creation of a Task object.

    Validates that a task is created with the correct attributes, including
    the task title, associated project, user, and default is_done status.
    """
    user = User.objects.create_user(username="testuser", password="testpass")
    project = Project.objects.create(user=user, name="Test Project", project_date="2025-02-10")
    task = Task.objects.create(project=project, title="Test Task", deadline=datetime.now(), user=user)

    # Assertions to ensure the task is correctly created
    assert task.title == "Test Task"
    assert task.project == project
    assert task.is_done is False
