from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
from rest_framework import status, serializers
from actionvim.models import User
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class BasicProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "username", "avatar", "phone"]
    

class LoginAPIView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                data={
                    "detail": "Please provide valid input",
                    "errors": serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        auth_data = serializer.validated_data
        user = authenticate(request, **auth_data)
        if not user:
            return Response(
                data={"detail": "Please enter valid credentials"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        profile_serializer = BasicProfileSerializer(user)
        login(request, user)
        return Response(
            data={
                "detail": "Login success",
                "user": profile_serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = BasicProfileSerializer(user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class LogoutAPIView(APIView):
    def get(self, request):
        logout(request)
        return Response(
            data={"detail": "You have been logged out!"}, status=status.HTTP_200_OK
        )
