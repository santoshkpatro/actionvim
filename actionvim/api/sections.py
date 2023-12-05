from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.db.models import Prefetch, F
from django.db import transaction
from django.utils import timezone

from actionvim.utils import cast_to_boolean
from actionvim.models import Project, Section, Task, User


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "avatar"]


class TaskSerializer(serializers.ModelSerializer):
    members = MemberSerializer(many=True)

    class Meta:
        model = Task
        fields = ["id", "title", "public_id", "members", "position", "created_at"]


class TaskCreateSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()
    position = serializers.IntegerField(required=False)


class SectionSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True)

    class Meta:
        model = Section
        fields = ["id", "title", "position", "created_at", "tasks"]


class SectionCreateSerializer(serializers.Serializer):
    title = serializers.CharField()
    position = serializers.IntegerField(required=False)


class TaskSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ["id", "title", "position", "created_at"]


class TaskDetailSerializer(serializers.ModelSerializer):
    section = TaskSectionSerializer()

    class Meta:
        model = Task
        fields = ["id", "title", "public_id", "position", "section", "created_at"]


class SectionUpdateSerializer(serializers.Serializer):
    title = serializers.CharField(required=False)
    position = serializers.IntegerField(required=False)


class SectionListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, project_public_id):
        project: Project = request.user.projects.filter(
            public_id=project_public_id
        ).first()
        if project is None:
            return Response(
                data={"detail": "No project found with the given public_id"},
                status=status.HTTP_404_NOT_FOUND,
            )

        create_serializer = SectionCreateSerializer(data=request.data)
        if not create_serializer.is_valid():
            return Response(
                data=create_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )

        data = create_serializer.validated_data
        section = Section(
            title=data.get("title"),
            position=data.get(
                "position",
                project.sections.filter(archived_at__isnull=True).count() + 1,
            ),
            project=project,
        )

        with transaction.atomic():
            Section.objects.filter(
                project=project, position__gte=section.position
            ).update(position=F("position") + 1)
            section.save()
        serializer = SectionSerializer(section)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, project_public_id):
        project: Project = request.user.projects.filter(
            public_id=project_public_id
        ).first()
        if project is None:
            return Response(
                {"detail": "No project found with the given public_id"},
                status=status.HTTP_404_NOT_FOUND,
            )

        archived = request.query_params.get("archived", False)
        member_usernames = request.query_params.get("member_usernames")
        task_queryset = Task.objects.prefetch_related("members").order_by("position")
        if member_usernames:
            task_queryset = task_queryset.filter(
                members__username__in=member_usernames.split(",")
            )
        sections = (
            Section.objects.filter(
                project=project, archived_at__isnull=not cast_to_boolean(archived)
            )
            .prefetch_related(
                Prefetch(
                    "tasks",
                    queryset=task_queryset,
                )
            )
            .order_by("position")
        )

        serializer = SectionSerializer(sections, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class SectionTaskListCreateAPIView(APIView):
    def get(self, request, project_public_id, section_id):
        project: Project = request.user.projects.filter(
            public_id=project_public_id
        ).first()
        if project is None:
            return Response(
                {"detail": "No project found with the given public_id"},
                status=status.HTTP_404_NOT_FOUND,
            )

        section = Section.objects.filter(project=project, id=section_id).first()
        if section is None:
            return Response(
                {"detail": "No section found with the given id"},
                status=status.HTTP_404_NOT_FOUND,
            )

        tasks = Task.objects.filter(project=project, section=section).order_by(
            "position"
        )
        serializer = TaskSerializer(tasks, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request, project_public_id, section_id):
        create_serializer = TaskCreateSerializer(data=request.data)
        if not create_serializer.is_valid():
            return Response(
                data={
                    "detail": "Please enter valid task create details!",
                    "errors": create_serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        project: Project = request.user.projects.filter(
            public_id=project_public_id
        ).first()
        if project is None:
            return Response(
                {"detail": "No project found with the given public_id"},
                status=status.HTTP_404_NOT_FOUND,
            )

        section = Section.objects.filter(project=project, id=section_id).first()
        if section is None:
            return Response(
                {"detail": "No section found with the given id"},
                status=status.HTTP_404_NOT_FOUND,
            )

        new_task_data = create_serializer.validated_data
        task = Task.objects.create(**new_task_data, section=section, project=project)

        serializer = TaskCreateSerializer(task)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class SectionDetailAPIView(APIView):
    def get(self, request, project_public_id, section_id):
        project: Project = request.user.projects.filter(
            public_id=project_public_id
        ).first()
        if project is None:
            return Response(
                {"detail": "No project found with the given public_id"},
                status=status.HTTP_404_NOT_FOUND,
            )

        section = (
            Section.objects.filter(project=project, id=section_id)
            .prefetch_related(
                Prefetch(
                    "tasks",
                    queryset=Task.objects.prefetch_related("members").order_by(
                        "position"
                    ),
                )
            )
            .first()
        )
        if section is None:
            return Response(
                {"detail": "No section found with the given id"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = SectionSerializer(section)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, project_public_id, section_id):
        update_serializer = SectionUpdateSerializer(data=request.data)
        if not update_serializer.is_valid():
            return Response(
                data={
                    "detail": "Please enter valid for updating project",
                    "errors": update_serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        project: Project = request.user.projects.filter(
            public_id=project_public_id
        ).first()
        if project is None:
            return Response(
                {"detail": "No project found with the given public_id"},
                status=status.HTTP_404_NOT_FOUND,
            )

        section: Section = Section.objects.filter(
            project=project, id=section_id
        ).first()
        if section is None:
            return Response(
                {"detail": "No section found with the given id"},
                status=status.HTTP_404_NOT_FOUND,
            )
        updated_data = update_serializer.validated_data
        new_position = updated_data.get("position", None)
        old_position = section.position
        for field, new_value in updated_data.items():
            setattr(section, field, new_value)
        with transaction.atomic():
            if new_position:
                if new_position > old_position:
                    Section.objects.filter(
                        project=project,
                        position__gt=old_position,
                        position__lte=new_position,
                    ).update(position=F("position") - 1)
                elif new_position < old_position:
                    Section.objects.filter(
                        project=project, position__gte=new_position
                    ).update(position=F("position") + 1)
            section.save(update_fields=updated_data.keys())

        serializer = SectionSerializer(section)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, project_public_id, section_id):
        project: Project = request.user.projects.filter(
            public_id=project_public_id
        ).first()
        if project is None:
            return Response(
                {"detail": "No project found with the given public_id"},
                status=status.HTTP_404_NOT_FOUND,
            )

        section: Section = Section.objects.filter(
            project=project, id=section_id
        ).first()
        if section is None:
            return Response(
                {"detail": "No section found with the given id"},
                status=status.HTTP_404_NOT_FOUND,
            )

        with transaction.atomic():
            Section.objects.filter(
                project=project, position__gt=section.position
            ).update(position=F("position") - 1)
            section.delete()

        return Response(
            data={"detail": "Section got deleted"}, status=status.HTTP_204_NO_CONTENT
        )


class SectionArchiveAPIView(APIView):
    def patch(self, request, project_public_id, section_id):
        project: Project = request.user.projects.filter(
            public_id=project_public_id
        ).first()
        if project is None:
            return Response(
                {"detail": "No project found with the given public_id"},
                status=status.HTTP_404_NOT_FOUND,
            )

        section = Section.objects.filter(
            project=project, id=section_id, archived_at__isnull=True
        ).first()
        if section is None:
            return Response(
                {"detail": "No section found with the given id"},
                status=status.HTTP_404_NOT_FOUND,
            )

        section.archived_at = timezone.now()
        section.archived_position = section.position
        section.position = None

        with transaction.atomic():
            Section.objects.filter(
                project=project, position__gt=section.archived_position
            ).update(position=F("position") - 1)
            section.save(update_fields=["archived_at", "archived_position", "position"])

        return Response(
            data={"detail": "Section has been archived"},
            status=status.HTTP_204_NO_CONTENT,
        )


class SectionRestoreAPIView(APIView):
    def patch(self, request, project_public_id, section_id):
        project: Project = request.user.projects.filter(
            public_id=project_public_id
        ).first()
        if project is None:
            return Response(
                {"detail": "No project found with the given public_id"},
                status=status.HTTP_404_NOT_FOUND,
            )

        section = (
            Section.objects.filter(
                project=project, id=section_id, archived_at__isnull=False
            )
            .prefetch_related(
                Prefetch(
                    "tasks",
                    queryset=Task.objects.prefetch_related("members").order_by(
                        "position"
                    ),
                )
            )
            .first()
        )
        if section is None:
            return Response(
                {"detail": "No archived section found with the given id"},
                status=status.HTTP_404_NOT_FOUND,
            )

        section.archived_at = None
        section.position = section.archived_position
        section.archived_position = None

        with transaction.atomic():
            Section.objects.filter(
                project=project, position__gte=section.position
            ).update(position=F("position") + 1)
            section.save(update_fields=["archived_at", "archived_position", "position"])

        serializer = SectionSerializer(section)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
