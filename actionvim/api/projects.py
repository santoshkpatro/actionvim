from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from actionvim.models import Project, User


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "avatar"]


class ProjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "public_id", "title", "task_count", "created_at"]


class ProjectDetailSerializer(serializers.ModelSerializer):
    members = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = [
            "id",
            "public_id",
            "title",
            "description",
            "task_count",
            "task_prefix",
            "created_at",
            "members",
        ]

    def get_members(self, project):
        members = User.objects.filter(user_permissions__project=project)
        serializer = MemberSerializer(members, many=True)
        return serializer.data


class ProjectListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        projects = request.user.projects.all()
        serializer = ProjectListSerializer(projects, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class ProjectDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, project_public_id):
        project = request.user.projects.filter(public_id=project_public_id).first()
        serializer = ProjectDetailSerializer(project)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
