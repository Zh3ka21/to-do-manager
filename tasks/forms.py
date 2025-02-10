"""
Forms for the tasks app, including forms for managing projects, tasks,
and user authentication (login/signup).
These forms include customization for placeholders and styling to improve
user experience on the frontend.
Requires:
    Django
    allauth
"""


from allauth.account.forms import LoginForm, SignupForm
from django import forms

from .models import Project, Task


class ProjectForm(forms.ModelForm):
    """
    Form for creating and updating a project.

    This form allows users to input and modify the 'name' field for projects.
    """

    class Meta:
        model = Project
        fields = ["name"]


class TaskForm(forms.ModelForm):
    """
    Form for creating and updating a task.

    This form allows users to input and modify task details, such as the
    associated project, title, deadline, completion status, and priority.
    """

    class Meta:
        model = Task
        fields = ["project", "title", "deadline", "is_done", "priority"]
        widgets = {
            "deadline": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }


class CustomLoginForm(LoginForm):
    """
    Custom login form that updates placeholder text and styling for input fields.

    This form customizes the default login form with specific placeholders and 
    CSS classes to improve the user interface.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["login"].widget.attrs.update({
            "placeholder": "Username or Email",
            "class": "form-control",
        })
        self.fields["password"].widget.attrs.update({
            "placeholder": "Password",
            "class": "form-control",
        })


class CustomSignupForm(SignupForm):
    """
    Custom signup form that updates placeholder text and styling for input fields.

    This form customizes the default signup form with specific placeholders and 
    CSS classes to improve the user interface during the signup process.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({
            "placeholder": "Username",
            "class": "form-control",
        })
        self.fields["email"].widget.attrs.update({
            "placeholder": "Email",
            "class": "form-control",
        })
        self.fields["password1"].widget.attrs.update({
            "placeholder": "Password",
            "class": "form-control",
        })
        self.fields["password2"].widget.attrs.update({
            "placeholder": "Confirm Password",
            "class": "form-control",
        })
