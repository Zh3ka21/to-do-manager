import pytest
from tasks.models import Project, Task
from django.contrib.auth import get_user_model
from datetime import datetime

User = get_user_model()


@pytest.mark.django_db
def test_create_project():
    user = User.objects.create_user(username="testuser", password="testpass")
    project = Project.objects.create(user=user, name="Test Project", project_date="2025-02-10")
    
    assert project.name == "Test Project"
    assert project.user == user


@pytest.mark.django_db
def test_create_task():
    user = User.objects.create_user(username="testuser", password="testpass")
    project = Project.objects.create(user=user, name="Test Project", project_date="2025-02-10")
    task = Task.objects.create(project=project, title="Test Task", deadline=datetime.now(), user=user)

    assert task.title == "Test Task"
    assert task.project == project
    assert task.is_done is False
