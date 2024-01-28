from rest_framework import viewsets
from .models import Task, Comment
from .serializers import (
    TaskSerializer,
    CommentSerializer,
    AssignTaskSerializer,
    TaskProgressReportSerializer,
    UserActivityReportSerializer,
    TaskCompletionRateOverTimeSerializer,
)
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from utils.permissions import IsAPIKEYAuthenticated
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db.models import Q
from utils.report import *


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAPIKEYAuthenticated, IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "admin":
            return Task.objects.all()
        elif user.role == "user":
            return Task.objects.filter(Q(created_by=user) | Q(is_private=False))


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAPIKEYAuthenticated, IsAuthenticated]


class TaskReportView(APIView):
    def get(self, request, *args, **kwargs):
        completed_tasks_count = Task.objects.filter(completion_status=True).count()
        data = {
            "completed_tasks_count": completed_tasks_count,
            # Add more reporting data as needed
        }

        return Response(data)


class TaskProgressReportAPIView(generics.RetrieveAPIView):
    serializer_class = TaskProgressReportSerializer

    def retrieve(self, request, *args, **kwargs):
        report = task_progress_report()  # Implement the function to generate the report
        serializer = self.get_serializer(report)
        return Response(serializer.data)


class UserActivityReportAPIView(generics.RetrieveAPIView):
    serializer_class = UserActivityReportSerializer

    def retrieve(self, request, *args, **kwargs):
        report = user_activity_report()  # Implement the function to generate the report
        serializer = self.get_serializer(report)
        return Response(serializer.data)


class TaskCompletionRateOverTimeAPIView(generics.RetrieveAPIView):
    serializer_class = TaskCompletionRateOverTimeSerializer

    def retrieve(self, request, *args, **kwargs):
        report = (
            task_completion_rate_over_time()
        )  # Implement the function to generate the report
        serializer = self.get_serializer(report)
        return Response(serializer.data)
