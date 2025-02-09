from datetime import date, datetime
from typing import Optional

from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models


class User(AbstractUser):
    pass

class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    project_date = models.DateField()
    deleted = models.BooleanField(default=False)

    @classmethod
    def get_project_for_date(cls, user: User, selected_date: str) -> Optional['Project']:
        """Get project for a specific date and user."""
        try:
            return cls.objects.get(user=user, project_date=selected_date, deleted=False)
        except cls.DoesNotExist:
            return None

    @classmethod
    def get_project_dates(cls, user: User, year: int, month: int) -> list[str]:
        """Get all project dates for a specific month and year."""
        from calendar import monthrange
        _, last_day = monthrange(year, month)
        start_date = date(year, month, 1)
        end_date = date(year, month, last_day)

        projects = cls.objects.filter(
            user=user,
            project_date__range=[start_date, end_date],
            deleted=False,
        ).values_list('project_date', flat=True)

        return [d.strftime('%Y-%m-%d') for d in projects]

    @classmethod
    def create_new_project(cls, user: User, name: str, project_date: str) -> tuple[bool, Optional['Project'], Optional[str]]:
        """Create a new project if one doesn't exist for the date."""
        if not name.strip():
            return False, None, "Project title cannot be empty"

        existing_project = cls.objects.filter(user=user, project_date=project_date, deleted=False).first()
        if existing_project:
            return False, None, "You already have a project for this date"

        project = cls.objects.create(
            user=user,
            name=name.strip(),
            project_date=project_date,
            deleted=False
        )
        return True, project, None

    def update_project(self, new_name: str) -> tuple[bool, Optional[str]]:
        """Update the project's name."""
        if not new_name.strip():
            return False, "Project name cannot be empty"

        self.name = new_name.strip()
        self.save()
        return True, None

    def soft_delete(self) -> None:
        """Soft delete the project."""
        self.deleted = True
        self.save()

    def __str__(self) -> str:
        return f"Project: {self.name}"

class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=255)
    deadline = models.DateTimeField()
    is_done = models.BooleanField(default=False)
    priority = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @classmethod
    def create_task(cls, user: User, project: Project, title: str, deadline_time: Optional[str] = None) -> tuple[bool, Optional['Task'], Optional[str]]:
        """Create a new task."""
        if not title.strip():
            return False, None, "Task title is required"

        try:
            if deadline_time:
                deadline = datetime.strptime(deadline_time, "%H:%M")
            else:
                deadline = datetime.now()

            # Get lowest priority
            lowest_priority_task = cls.objects.filter(project=project).order_by('-priority').first()
            lowest_priority = lowest_priority_task.priority if lowest_priority_task else 0

            task = cls.objects.create(
                project=project,
                title=title.strip(),
                deadline=deadline,
                user=user,
                priority=lowest_priority + 1,
            )
            return True, task, None

        except ValueError:
            return False, None, "Invalid time format"

    def toggle_done(self) -> None:
        """Toggle the completion status of the task."""
        self.is_done = not self.is_done
        self.save()

    def update_title(self, new_title: str) -> tuple[bool, Optional[str]]:
        """Update the task's title."""
        if not new_title.strip():
            return False, "Title cannot be empty"

        self.title = new_title.strip()
        self.save()
        return True, None

    def move_priority(self, direction: str) -> bool:
        """Move task priority up or down."""
        tasks = Task.objects.filter(project=self.project).order_by('priority')
        task_list = list(tasks)
        task_index = task_list.index(self)

        if direction == 'up' and task_index > 0:
            other_task = task_list[task_index - 1]
        elif direction == 'down' and task_index < len(task_list) - 1:
            other_task = task_list[task_index + 1]
        else:
            return False

        self.priority, other_task.priority = other_task.priority, self.priority
        other_task.save()
        self.save()
        return True

    def __str__(self) -> str:
        status = "Done" if self.is_done else "Not done"
        return f"{self.title} | Priority: {self.priority} | Deadline: {self.deadline} | Status: {status}"
