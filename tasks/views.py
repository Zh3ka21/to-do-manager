from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .models import Project, Task


def base_view_handler(request: HttpRequest) -> HttpResponse:
    """Handle default URL routing."""
    if request.user.is_authenticated:
        projects = Project.objects.filter(user=request.user)
    else:
        projects = Project.objects.none()

    tasks = Task.objects.filter(project__in=projects)

    context = {
        'projects': projects,
        'tasks': tasks,
    }
    return render(request, "main.html", context)

def toggle_task(request: HttpRequest, task_id: int) -> HttpResponse:
    task = get_object_or_404(Task, id=task_id)

    # Toggle the task's completion status
    task.is_done = not task.is_done
    task.save()

    # Redirect back to the page after toggling
    return redirect(request.META.get('HTTP_REFERER', '/'))

def move_task(request: HttpRequest, task_id: int, direction: str):
    task = get_object_or_404(Task, id=task_id)

    # Get all tasks sorted by a field such as 'order' or 'created_at'
    tasks = Task.objects.all().order_by('priority')

    task_index = list(tasks).index(task)  # Find the current index of the task

    # Move the task up or down based on the direction
    if direction == 'up' and task_index > 0:
        task_to_swap = tasks[task_index - 1]
        task_to_swap.priority, task.priority = task.priority, task_to_swap.priority
        task_to_swap.save()
        task.save()
    elif direction == 'down' and task_index < len(tasks) - 1:
        task_to_swap = tasks[task_index + 1]
        task_to_swap.priority, task.priority = task.priority, task_to_swap.priority
        task_to_swap.save()
        task.save()

    # Redirect back to the page after moving the task
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def add_task(request) -> HttpResponse:
    """Add task to a project."""
    if request.method == "POST":
        print(request.POST)  # Debugging
        task_name = request.POST.get("task_name")
        if not task_name:
            return JsonResponse({'error': 'No task name provided'}, status=400)

        task = Task.objects.create(title=task_name, user=request.user)
        return render(request, 'task_partial.html', {'task': task})

    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def delete_task(request, task_id: int) -> HttpResponse:
    """Delete task from a project."""
    task = Task.objects.get(id=task_id, user=request.user)
    task.delete()
    return JsonResponse({'success': True})

@login_required
def edit_task(request, task_id: int) -> HttpResponse:
    """Edit a task in a project."""
    task = Task.objects.get(id=task_id, user=request.user)
    if request.method == 'GET':
        # Render a form or HTML snippet for editing
        return render(request, 'task_edit_partial.html', {'task': task})

    if request.method == 'POST':
        task.title = request.POST.get('task_name')
        task.save()
        return render(request, 'task_partial.html', {'task': task})
    return render(request, 'main.html')
