"""
Tests for views in the tasks app.

These tests validate the behavior of base and task creation views, ensuring that:
- Authenticated users can access the base view.
- A task can be successfully added to a project by an authenticated user.

Requires:
    pytest
    Django
"""

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from tasks.models import Project, Task

# Get the User model from Django
User = get_user_model()


@pytest.mark.django_db
def test_base_view_authenticated(client) -> None:
    """
    Test the base view with an authenticated user.

    Ensures that an authenticated user can access the base view successfully.
    """
    _ = User.objects.create_user(username="testuser", password="testpass")
    client.login(username="testuser", password="testpass")

    # Request the base view
    response = client.get(reverse("base_view_handler"))  # Adjust if necessary

    # Ensure the response status is 200 (OK)
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_task(client) -> None:
    """
    Test adding a task to a project.

    Ensures that an authenticated user can add a task to a project
    successfully and that the task is saved in the database.
    """
    user = User.objects.create_user(username="testuser", password="testpass")
    project = Project.objects.create(user=user, name="Test Project", project_date="2025-02-10")

    client.login(username="testuser", password="testpass")

    # Post request to add a new task
    response = client.post(reverse("add_task"), {
        "task_name": "New Task",
        "deadline_time": "12:00",
        "project_id": project.id,
        "date": "2025-02-10",
    })

    # Ensure the response status is 200 (OK) and the task is created
    assert response.status_code == 200
    assert Task.objects.filter(title="New Task").exists()
