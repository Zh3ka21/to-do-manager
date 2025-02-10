import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from tasks.models import Project, Task

User = get_user_model()


@pytest.mark.django_db
def test_base_view_authenticated(client):
    """Test base view with an authenticated user"""
    user = User.objects.create_user(username="testuser", password="testpass")
    client.login(username="testuser", password="testpass")

    response = client.get(reverse("base_view_handler"))  # Adjust if necessary
    assert response.status_code == 200


@pytest.mark.django_db
def test_add_task(client):
    """Test adding a task"""
    user = User.objects.create_user(username="testuser", password="testpass")
    project = Project.objects.create(user=user, name="Test Project", project_date="2025-02-10")

    client.login(username="testuser", password="testpass")

    response = client.post(reverse("add_task"), {
        "task_name": "New Task",
        "deadline_time": "12:00",
        "project_id": project.id,
        "date": "2025-02-10",
    })

    assert response.status_code == 200
    assert Task.objects.filter(title="New Task").exists()
