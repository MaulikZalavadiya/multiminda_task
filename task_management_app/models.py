from django.db import models
from userApp.models import *


class Task(models.Model):
    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    priority = models.CharField(
        max_length=20, choices=PRIORITY_CHOICES, default="medium"
    )
    due_date = models.DateField()
    completion_status = models.BooleanField(default=False)
    is_private = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        ApplicationUser,
        on_delete=models.CASCADE,
        related_name="created_task_user",
        null=True,
    )
    updated_by = models.ForeignKey(
        ApplicationUser,
        on_delete=models.CASCADE,
        related_name="updated_task_user",
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class AssignTask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="assign_task")
    assign_user = models.ForeignKey(
        ApplicationUser, on_delete=models.CASCADE, related_name="assign_task_user"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    user = models.ForeignKey(ApplicationUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
