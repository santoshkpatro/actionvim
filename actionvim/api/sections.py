from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.db.models import Prefetch

from actionvim.models import Project, Section, Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "title", "public_id", "position", "created_at"]


class SectionSerializer(serializers.ModelSerializer):
    tasks = TaskSerializer(many=True)

    class Meta:
        model = Section
        fields = ["id", "title", "position", "created_at", "tasks"]


class SectionCreateSerializer(serializers.Serializer):
    title = serializers.CharField()


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
            **data, position=project.sections.all().count() + 1, project=project
        )
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

        sections = (
            Section.objects.filter(project=project)
            .prefetch_related(
                Prefetch("tasks", queryset=Task.objects.order_by("position"))
            )
            .order_by("position")
        )
        serializer = SectionSerializer(sections, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)



class SectionTaskListAPIView(APIView):
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
        
        tasks = Task.objects.filter(project=project, section=section).order_by("position")
        serializer = TaskSerializer(tasks, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)
