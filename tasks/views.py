from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProjectForm, TaskForm
from .models import Project, Task


def project_list_view(request: HttpRequest) -> HttpResponse:
    """View to see a list of projects."""
    projects = Project.objects.all()
    context = {"projects": projects}
    return render(request, "projects/projects_list.html", context)

def create_project_view(request: HttpRequest) -> HttpResponse:
    """View to create a new project."""
    if request.method == "POST":
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("project_list")  # Redirect to a project list view
    else:
        form = ProjectForm()
    return render(request, "projects/create_project.html", {"form": form})

def update_project_view(request: HttpRequest, project_id: int) -> HttpResponse:
    """View to update an existing project."""
    project = get_object_or_404(Project, id=project_id)
    if request.method == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect("project_detail", project_id=project.id)
    else:
        form = ProjectForm(instance=project)
    return render(request, "projects/update_project.html", {"form": form, "project": project})

def delete_project_view(request: HttpRequest, project_id: int) -> HttpResponse:
    """View to delete a project."""
    project = get_object_or_404(Project, id=project_id)
    if request.method == "POST":
        project.delete()
        return redirect("project_list")  # Redirect to project list view
    return render(request, "projects/delete_project.html", {"project": project})

def project_detail_view(request: HttpRequest, project_id: int) -> HttpResponse:
    """View to display a single project and its tasks."""
    project = get_object_or_404(Project, id=project_id)
    tasks = project.tasks.all()
    return render(request, "projects/project_detail.html", {"project": project, "tasks": tasks})

def add_task_to_project(request: HttpRequest, project_id: int) -> HttpResponse:
    """View to add a task to a specific project."""
    project = get_object_or_404(Project, id=project_id)

    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            return redirect("project_detail", project_id=project.id)
    else:
        form = TaskForm()

    return render(request, "tasks/add_task.html", {"form": form, "project": project})

def update_task_in_project(request: HttpRequest, project_id: int, task_id: int) -> HttpResponse:
    """View to update a task within a specific project."""
    project = get_object_or_404(Project, id=project_id)
    task = get_object_or_404(Task, id=task_id, project=project)  # Ensure task belongs to project

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("project_detail", project_id=project.id)
    else:
        form = TaskForm(instance=task)

    return render(request, "tasks/update_task.html", {"form": form, "project": project, "task": task})

def delete_task_from_project(request: HttpRequest, project_id: int, task_id: int) -> HttpResponse:
    """View to delete a task from a specific project."""
    project = get_object_or_404(Project, id=project_id)
    task = get_object_or_404(Task, id=task_id, project=project)  # Ensure task belongs to project

    if request.method == "POST":
        task.delete()
        return redirect("project_detail", project_id=project.id)

    return render(request, "tasks/delete_task.html", {"project": project, "task": task})



