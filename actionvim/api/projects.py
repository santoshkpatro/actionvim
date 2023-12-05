from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from actionvim.models import Project, User, Permission


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "avatar"]


class ProjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "public_id", "title", "task_count", "created_at"]


class ProjectUpdateSerializer(serializers.Serializer):
    title = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    task_prefix = serializers.CharField(required=False, max_length=20)


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
        if project is None:
            return Response(
                data={"detail": "No project found with the given public ID"},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = ProjectDetailSerializer(project)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, project_public_id):
        update_serializer = ProjectUpdateSerializer(data=request.data)
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
                data={"detail": "No project found with the given public ID"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Checking for project admin permission.
        permission: Permission = Permission.objects.filter(
            user=request.user, project=project
        ).first()
        if permission is None or permission.role != permission.Role.ADMIN:
            return Response(
                data={
                    "detail": "You do not have enough permission to perform this action"
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        updated_data = update_serializer.validated_data
        for field, new_value in updated_data.items():
            setattr(project, field, new_value)
        project.save(update_fields=updated_data.keys())
        serializer = ProjectDetailSerializer(project)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, project_public_id):
        project: Project = request.user.projects.filter(
            public_id=project_public_id
        ).first()
        if project is None:
            return Response(
                data={"detail": "No project found with the given public ID"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Checking for project admin permission.
        permission: Permission = Permission.objects.filter(
            user=request.user, project=project
        ).first()
        if permission is None or permission.role != permission.Role.ADMIN:
            return Response(
                data={
                    "detail": "You do not have enough permission to perform this action"
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        project.delete()
        return Response(
            data={"detail": "Project got deleted"}, status=status.HTTP_204_NO_CONTENT
        )
