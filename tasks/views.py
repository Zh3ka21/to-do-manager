import calendar
import json
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.forms import ValidationError
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.utils.timezone import make_aware, now

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

        # Counting lowest priority task to append to bottom of task list
        lowest_priority_task = Task.objects.filter(project=project).order_by('-priority').first()
        lowest_priority = lowest_priority_task.priority if lowest_priority_task else 0

        task = Task.objects.create(
            project=project,
            title=title,
            deadline=deadline,
            user=request.user,
            priority = lowest_priority+1,
        )

        return render(request, 'partials/task_partial.html', {'task': task})
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
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == "POST":
        new_title = request.POST.get("title")
        if new_title:
            task.title = new_title
            task.save()
        return render(request, "partials/task_partial.html", {"task": task})
    return HttpResponse(status=400)

@login_required
def project_dates(request):
    try:
        month = int(request.GET.get('month'))
        year = int(request.GET.get('year'))

        # Get the first and last day of the month
        _, last_day = calendar.monthrange(year, month)
        start_date = datetime(year, month, 1).date()
        end_date = datetime(year, month, last_day).date()

        # Query for projects using project_date field
        projects = Project.objects.filter(
            user=request.user,
            project_date__range=[start_date, end_date]
        ).values_list('project_date', flat=True)
        
        # Convert dates to strings
        dates = [d.strftime('%Y-%m-%d') for d in projects]
        return JsonResponse(dates, safe=False)
    except (ValueError, TypeError) as e:
        return JsonResponse({'error': str(e)}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def create_project(request):
    try:
        # Use request.POST instead of json.loads(request.body)
        project_date = datetime.strptime(
            request.POST.get('date'), 
            '%Y-%m-%d'
        ).date()

        project = Project.objects.create(
            user=request.user,
            name=request.POST.get('name', f'Project for {project_date}'),
            project_date=project_date,
        )

        return JsonResponse({
            'message': f"Project '{project.name}' created successfully",
        })


    except ValidationError as e:
        return JsonResponse({'error': str(e)}, status=400)
    except Exception as e:
        print(f"Error creating project: {str(e)}")  # Add detailed logging
        return JsonResponse({'error': str(e)}, status=500)

