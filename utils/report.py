from django.db.models import Count
from django.db.models.functions import TruncDate
from django.utils.timezone import now
from task_management_app.models import *


def task_completion_rate_over_time():
    # Truncate the task completion date to the date part
    tasks = Task.objects.annotate(completion_date=TruncDate("updated_at"))
    # Count completed tasks per day
    completion_over_time = (
        tasks.filter(completion_status=True)
        .values("completion_date")
        .annotate(task_count=Count("id"))
    )
    # Return the report
    report = {
        "completion_over_time": completion_over_time,
    }
    return report


def user_activity_report():
    # Count the tasks created by each user
    user_activity = Task.objects.values("created_by__username").annotate(
        task_count=Count("id")
    )
    # Return the report
    report = {
        "user_activity": user_activity,
    }
    return report


def task_progress_report():
    # Count the total number of tasks
    total_tasks = Task.objects.count()
    # Count the number of completed tasks
    completed_tasks = Task.objects.filter(completion_status=True).count()
    # Calculate completion rate
    completion_rate = (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0
    # Return the report
    report = {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "completion_rate": completion_rate,
    }
    return report
