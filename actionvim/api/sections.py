from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from actionvim.models import Project, Section


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ["id", "title", "position", "created_at"]


class SectionCreateSerializer(serializers.Serializer):
    title = serializers.CharField()


class SectionListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, public_id):
        project: Project = request.user.projects.filter(public_id=public_id).first()
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
            **data, position=project.project_sections.all().count() + 1, project=project
        )
        section.save()
        serializer = SectionSerializer(section)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, public_id):
        project: Project = request.user.projects.filter(public_id=public_id).first()
        if project is None:
            return Response(
                {"detail": "No project found with the given public_id"},
                status=status.HTTP_404_NOT_FOUND,
            )

        sections = Section.objects.filter(project=project).order_by("position")
        print(sections)
        serializer = SectionSerializer(sections, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)
