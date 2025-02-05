from allauth.account.forms import LoginForm, SignupForm
from django import forms
from django.forms import ValidationError

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

class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize placeholders
        self.fields['login'].widget.attrs.update({
            'placeholder': 'Username or Email',
            'class': 'form-control',
        })
        self.fields['password'].widget.attrs.update({
            'placeholder': 'Password',
            'class': 'form-control',
        })

class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize placeholders
        self.fields['username'].widget.attrs.update({
            'placeholder': 'Username',
            'class': 'form-control',
        })
        self.fields['email'].widget.attrs.update({
            'placeholder': 'Email',
            'class': 'form-control',
        })
        self.fields['password1'].widget.attrs.update({
            'placeholder': 'Password',
            'class': 'form-control',
        })
        self.fields['password2'].widget.attrs.update({
            'placeholder': 'Confirm Password',
            'class': 'form-control',
        })
