from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import F
from django.db import transaction
from actionvim.models import Project, Section, Task, User


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ["id", "title", "position", "created_at"]


class TaskListSerializer(serializers.ModelSerializer):
    section = SectionSerializer()

    class Meta:
        model = Task
        fields = ["id", "public_id", "section", "title", "position", "created_at"]


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "avatar"]


class TaskSerializer(serializers.ModelSerializer):
    section = SectionSerializer()
    members = MemberSerializer(many=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "public_id",
            "section",
            "title",
            "position",
            "description",
            "members",
            "updated_at",
            "created_at",
        ]


class TaskUpdateSerializer(serializers.Serializer):
    title = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    position = serializers.IntegerField(required=False)


class TaskListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, project_public_id):
        project: Project = request.user.projects.filter(
            public_id=project_public_id
        ).first()
        if project is None:
            return Response(
                data={"detail": "No project found with the given public_id"},
                status=status.HTTP_404_NOT_FOUND,
            )

        tasks = Task.objects.filter(project=project).select_related("section")
        serializer = TaskListSerializer(tasks, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class TaskDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, project_public_id, task_public_id):
        project: Project = request.user.projects.filter(
            public_id=project_public_id
        ).first()
        if project is None:
            return Response(
                data={"detail": "No project found with the given public_id"},
                status=status.HTTP_404_NOT_FOUND,
            )

        task: Task = (
            Task.objects.filter(project=project, public_id=task_public_id)
            .select_related("section")
            .prefetch_related("members")
            .first()
        )
        if task is None:
            return Response(
                data={"detail": "No task found with the given public_id"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = TaskSerializer(task)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, project_public_id, task_public_id):
        update_serializer = TaskUpdateSerializer(data=request.data)

        if not update_serializer.is_valid():
            return Response(
                data={
                    "detail": "Please enter valid order update details",
                    "errors": update_serializer.errors,
                }
            )

        project: Project = request.user.projects.filter(
            public_id=project_public_id
        ).first()
        if project is None:
            return Response(
                data={"detail": "No project found with the given public_id"},
                status=status.HTTP_404_NOT_FOUND,
            )

        task: Task = Task.objects.filter(
            project=project, public_id=task_public_id
        ).first()
        if task is None:
            return Response(
                data={"detail": "No task found with the given public_id"},
                status=status.HTTP_404_NOT_FOUND,
            )

        updated_data = update_serializer.validated_data
        new_position = updated_data.get("position", None)
        old_position = task.position
        for field, new_value in updated_data.items():
            setattr(task, field, new_value)

        with transaction.atomic():
            if new_position:
                Task.objects.filter(
                    project=project,
                    section=task.section,
                    position__gt=old_position,
                    position__lte=new_position,
                ).update(position=F("position") - 1)
            task.save(update_fields=updated_data.keys())

        serializer = TaskSerializer(task)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
