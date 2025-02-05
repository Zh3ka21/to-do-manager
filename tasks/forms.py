from django import forms

from .models import Project, Task


class ProjectForm(forms.ModelForm):
    """Form for creating and updating a project."""

    class Meta:
        model = Project
        fields = ["name"]


class TaskForm(forms.ModelForm):
    """Form for creating and updating a task."""
    class Meta:
        model = Task
        fields = ["title", "deadline", "priority", "user", "is_done"]
        widgets = {
            "deadline": forms.DateTimeInput(attrs={"type": "datetime-local"}),  
        }
