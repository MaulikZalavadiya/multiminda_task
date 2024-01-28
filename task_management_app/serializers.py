from rest_framework import serializers
from .models import Task, Comment, AssignTask
from userApp.models import ApplicationUser
from userApp.serializers import AuthorizeUserSerializer
from rest_framework.exceptions import ValidationError


class AssignTaskSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        user_record = super().to_representation(instance)
        user_record["assign_user"] = AuthorizeUserSerializer(instance.assign_user).data
        return user_record

    class Meta:
        model = AssignTask
        exclude = ["id", "created_at", "updated_at", "task"]


class CommentSerializer(serializers.ModelSerializer):
    task = serializers.IntegerField(write_only=True)

    def to_representation(self, instance):
        user_record = super().to_representation(instance)
        user_record["comment_user"] = AuthorizeUserSerializer(instance.user).data
        return user_record

    class Meta:
        model = Comment
        fields = ["id", "text", "task"]

    def create(self, validated_data):
        request_user = self.context["request"].user
        allocated_user = list(
            AssignTask.objects.filter(task=validated_data["task"]).values_list(
                "assign_user", flat=True
            )
        )
        if request_user.id in allocated_user or request_user.role == "admin":
            validated_data["task"] = Task.objects.get(pk=validated_data["task"])
            validated_data["user_id"] = request_user.id
            return super().create(validated_data)
        raise ValidationError(
            "you can't comment this task only allocated user can comment. "
        )


class TaskSerializer(serializers.ModelSerializer):
    assign_user = serializers.ListSerializer(
        child=serializers.PrimaryKeyRelatedField(
            queryset=ApplicationUser.objects.all()
        ),
        write_only=True,
    )

    def to_representation(self, instance):
        task_record = super().to_representation(instance)
        assign_task_queryset = instance.assign_task.all()

        if not assign_task_queryset.exists():
            task_record["assign_task"] = []
        else:
            task_record["assign_task"] = AssignTaskSerializer(
                assign_task_queryset, many=True
            ).data
        task_comment_queryset = instance.comments.all()
        if not task_comment_queryset.exists():
            task_record["task_comment"] = []
        else:
            task_record["task_comment"] = CommentSerializer(
                task_comment_queryset, many=True
            ).data

        task_record["created_by"] = instance.created_by.username
        task_record["due_date"] = instance.due_date.strftime("%d-%m-%Y")
        task_record["created_at"] = instance.created_at.strftime("%d-%m-%Y")
        return task_record

    class Meta:
        model = Task
        exclude = []

    def create(self, validated_data):
        validated_data["created_by"] = self.context["request"].user
        assign_user_list = validated_data.pop("assign_user", [])
        task_id = super().create(validated_data)
        for user in assign_user_list:
            AssignTask.objects.create(task=task_id, assign_user=user)
        return task_id


class TaskProgressReportSerializer(serializers.Serializer):
    total_tasks = serializers.IntegerField()
    completed_tasks = serializers.IntegerField()
    completion_rate = serializers.FloatField()


class UserActivityReportSerializer(serializers.Serializer):
    user_activity = serializers.ListField(child=serializers.DictField())


class TaskCompletionRateOverTimeSerializer(serializers.Serializer):
    completion_over_time = serializers.ListField(child=serializers.DictField())
