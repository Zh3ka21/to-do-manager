from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.timezone import now

from tasks.forms import TaskForm

from .models import Project, Task


def base_view_handler(request: HttpRequest) -> HttpResponse:
    """Handle default URL routing."""
    if request.user.is_authenticated:
        projects = Project.objects.filter(user=request.user)
    else:
        projects = Project.objects.none()

    tasks = Task.objects.filter(project__in=projects).order_by('priority')

    context = {
        'projects': projects,
        'tasks': tasks,
    }
    return render(request, "main.html", context)

@login_required
def toggle_task_done(request, task_id: int) -> HttpResponse:
    """Toggle the completion status of a task."""
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.is_done = not task.is_done  # Toggle status
    task.save()
    return render(request, 'partials/task_partial.html', {'task': task})

@login_required
def add_task(request):
    if request.method == "POST":
        title = request.POST.get("task_name")  # Match input field name
        deadline_time = request.POST.get("deadline_time")
        project_name = request.POST.get("project_name")

        if not title:
            return JsonResponse({'error': 'Task title is required'}, status=400)

        try:
            project = Project.objects.get(name=project_name, user=request.user)
        except Project.DoesNotExist:
            return JsonResponse({'error': 'Invalid project'}, status=400)


        if deadline_time:
            try:
                deadline = datetime.strptime(deadline_time, "%H:%M").time()
                deadline = datetime.combine(now().date(), deadline)  
            except ValueError:
                return JsonResponse({'error': 'Invalid time format'}, status=400)
        else:
            deadline = now()

        _ = Task.objects.create(
            project=project,
            title=title,
            deadline=deadline,
            user=request.user,
        )

        tasks = Task.objects.filter(project__in=project).order_by('priority')
        return render(request, 'partials/task_list.html', {'tasks': tasks})
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@login_required
def delete_task(request, task_id: int) -> HttpResponse:
    """Delete task dynamically using HTMX."""
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.delete()
    return JsonResponse({'success': True})

def move_task(request: HttpRequest, task_id: int, direction: str):
    task = get_object_or_404(Task, id=task_id)

    # Get all tasks sorted by a field  'priority'
    tasks = Task.objects.all().order_by('priority')

    task_index = list(tasks).index(task)

    # Move the task up or down
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

    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
def edit_task(request, task_id: int) -> HttpResponse:
    task = get_object_or_404(Task, id=task_id)

    if request.method == "POST":
        # Update the task title
        new_title = request.POST.get("title")
        if new_title:
            task.title = new_title
            task.save()
            return HttpResponse(status=204)  # No content response for HTMX
        else:
            return HttpResponse("Title is required", status=400)

    # Render the edit form for GET requests
    return render(request, "partials/edit_task_form.html", {"task": task})
