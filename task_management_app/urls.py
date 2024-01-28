from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register("tasks", TaskViewSet, basename="task")
router.register("comments", CommentViewSet, basename="comment")

urlpatterns = [
    path("", include(router.urls)),
    path("report/", TaskReportView.as_view(), name="task-report"),
    path(
        "task-progress-report/",
        TaskProgressReportAPIView.as_view(),
        name="task-progress-report",
    ),
    path(
        "user-activity-report/",
        UserActivityReportAPIView.as_view(),
        name="user-activity-report",
    ),
    path(
        "task-completion-rate-over-time/",
        TaskCompletionRateOverTimeAPIView.as_view(),
        name="task-completion-rate-over-time",
    ),
    # Add more URLs as needed
]
