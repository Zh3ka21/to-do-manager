from typing import Optional

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def add_task(self, task: "Task") -> None:
        """Add on a task to the project.

        :param task: The Task object to be added.
        """
        task.project = self
        task.save()

    def update_project(self, new_name: str) -> None:
        """Update on the project's name.

        :param new_name: The new name for the project.
        """
        self.name = new_name
        self.save()

    def delete_project(self) -> None:
        """Delete the project."""
        self.delete()

    def __str__(self) -> str:
        return f"Project: {self.name}\n"


class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    title = models.CharField(max_length=255)
    deadline = models.DateTimeField()
    is_done = models.BooleanField(default=False)
    priority = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def update_task(self, new_title: str = "", new_deadline: Optional[str] = None) -> None:
        """Update on the task's title or deadline.

        :param new_title: The new title for the task (optional).
        :param new_deadline: The new deadline for the task (optional).
        """
        if new_title:
            self.title = new_title
        if new_deadline:
            self.deadline = new_deadline
        self.save()

    def mark_done(self) -> None:
        """Mark the task as done."""
        self.is_done = True
        self.save()

    def set_priority(self, priority: int) -> None:
        """Set the priority for the task.

        :param priority: The priority value for the task.
        """
        self.priority = priority
        self.save()

    def __str__(self) -> str:
        status = "Done" if self.is_done else "Not done"
        return f"{self.title} | Priority: {self.priority} | Deadline: {self.deadline} | Status: {status}"
