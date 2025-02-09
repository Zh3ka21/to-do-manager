import calendar
from datetime import date, datetime

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.forms import model_to_dict
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.timezone import now

from .models import Project, Task


def base_view_handler(request: HttpRequest) -> HttpResponse:
    """Handle default URL routing and display projects/tasks for a selected date."""

    selected_date = request.GET.get("date", date.today().strftime('%Y-%m-%d'))
    project = None
    tasks = Task.objects.none()  # Default to no tasks

    if request.user.is_authenticated:
        # Fetch the project for the selected date
        project = Project.get_project_for_date(request.user, selected_date)

        if project:
            # If a project exists, fetch tasks associated with that project
            tasks = project.tasks.filter(created_at__date=selected_date).order_by("priority")
        else:
            # If no project exists, check if there are tasks with no project (project__isnull=True)
            tasks = Task.objects.filter(
                Q(project__isnull=True, user=request.user),
                created_at__date=selected_date
            ).order_by("priority")

    # If no project or tasks were found, `tasks` will be an empty queryset.
    context = {
        "project": project,
        "tasks": tasks,
        "selected_date": selected_date,
    }

    return render(request, "main.html", context)

@login_required
def toggle_task_done(request, task_id) -> HttpResponse:
    """Toggle the completion status of a task."""
    task = get_object_or_404(Task, id=task_id, user=request.user)
    task.toggle_done()

    # Return the updated task HTML after the toggle
    return render(request, 'partials/task_partial.html', {'task': task})

@login_required
def add_task(request):
    if request.method == "POST":
        title = request.POST.get("task_name")
        deadline_time = request.POST.get("deadline_time")
        project_id = request.POST.get("project_id")
        selected_date = request.POST.get("date", now().date().strftime('%Y-%m-%d'))

        if not title:
            return JsonResponse({'error': 'Task title is required'}, status=400)

        # Find existing project for the date or use the provided project_id
        project = None
        if project_id:
            try:
                project = Project.objects.get(id=project_id, user=request.user, deleted=False)
            except Project.DoesNotExist:
                return JsonResponse({'error': 'Invalid project'}, status=400)
        else:
            project = Project.get_project_for_date(request.user, selected_date)

        # Handling deadline time
        try:
            deadline = datetime.strptime(deadline_time, "%H:%M").time() if deadline_time else now().time()
            deadline = datetime.combine(now().date(), deadline)
        except ValueError:
            return JsonResponse({'error': 'Invalid time format'}, status=400)

        # Determine priority
        lowest_priority_task = Task.objects.filter(
            Q(project=project) | Q(project__isnull=True, user=request.user, created_at__date=selected_date)
        ).order_by('-priority').first()
        lowest_priority = lowest_priority_task.priority if lowest_priority_task else 0

        # Create task (with or without a project)
        task = Task.objects.create(
            project=project,
            title=title.strip(),
            deadline=deadline,
            user=request.user,
            priority=lowest_priority + 1,
        )

        return render(request, 'partials/task_partial.html', {'task': task})
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@login_required
def delete_task(request, task_id: int) -> HttpResponse:
    """Delete task using HTMX."""
    if request.method == "POST":
        task = get_object_or_404(Task, id=task_id, user=request.user)
        task.delete()
        return HttpResponse("")  # Return empty response for HTMX delete
    return HttpResponse(status=405)  # Method not allowed

@login_required
def edit_task(request, task_id: int) -> HttpResponse:
    """Edit task using HTMX."""
    if request.method == "POST":
        try:
            task = get_object_or_404(Task, id=task_id, user=request.user)
            new_title = request.POST.get("title", "").strip()
            if not new_title:
                print("Title is empty!")
                return HttpResponse("Title cannot be empty", status=400)

            task.title = new_title
            task.save()
            return render(request, "partials/task_partial.html", {"task": task})

        except Exception as e:
            print("Error:", e)
            return HttpResponse("Something went wrong", status=500)

    return HttpResponse(status=405)


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
            project_date__range=[start_date, end_date],
            deleted=False,
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
    if request.method == "POST":
        project_name = request.POST.get("name", "").strip()
        project_date = request.POST.get("date")

        if not project_name:
            return JsonResponse({"error": "Project title cannot be empty"}, status=400)

        existing_project = Project.objects.filter(user=request.user, project_date=project_date, deleted=False).first()
        if existing_project:
            return JsonResponse({"error": "You already have a project for this date"}, status=400)

        # Get tasks for the given date
        tasks = Task.objects.filter(user=request.user, deadline__date=project_date, project__isnull=True)


        # Create the project
        project = Project.objects.create(
            user=request.user,
            name=project_name,
            project_date=project_date,
            deleted=False,
        )

        # Associate tasks with the project if any exist
        if tasks.exists():
            tasks.update(project=project)

        return JsonResponse(
            {
                "message": "Project created successfully",
            },
        )
    return JsonResponse({"error": "Invalid request"}, status=400)


@login_required
def get_tasks_for_date(request):
    date = request.GET.get("date")
    if not date:
        return JsonResponse({"error": "Date is required"}, status=400)

    # Fetch the project for the given date and user
    project = Project.objects.filter(user=request.user, project_date=date, deleted=False).first()

    # Fetch tasks that are either associated with the project or standalone (no project)
    if project:
        tasks_with_project = Task.objects.filter(project=project).values("id", "title", "is_done")

        tasks_without_project = Task.objects.filter(
            project__isnull=True,
            user=request.user, deadline=date,
        ).values("id", "title", "is_done")

        tasks = list(tasks_with_project) + list(tasks_without_project)
    else:
        tasks = Task.objects.filter(
            project__isnull=True,
            user=request.user,
            deadline__date=date,
        ).values("id", "title", "is_done")

    context = {
        "tasks": list(tasks),
        "project": model_to_dict(project) if project else None,
    }
    return JsonResponse({"context": context})

def update_project_name(request, project_id):
    if request.method == 'POST':
        project = Project.objects.get(id=project_id, deleted=False)
        new_name = request.POST.get('name')

        if new_name:
            project.update_project(new_name)
            return JsonResponse({'success': True, 'name': new_name})

        return JsonResponse({'error': 'Invalid name'})
    return JsonResponse({'error': 'Invalid request method'})

def soft_delete_project(request, project_id):
    if request.method == 'POST':
        project = Project.objects.get(id=project_id, deleted=False)
        project.soft_delete()
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Invalid request method'})
