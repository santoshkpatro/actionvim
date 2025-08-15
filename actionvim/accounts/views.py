from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework import status
from django.contrib.auth import login

from actionvim.accounts.models import User
from actionvim.accounts.serializers import (
    SignInSerializer,
    UserSerializer,
)
from actionvim.response import success_response, error_response


class AccountViewSet(ViewSet):
    def sign_in(self, request, *args, **kwargs):
        serializer = SignInSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(
                message="Invalid credentials",
                errors=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
        validated_data = serializer.validated_data
        user = User.objects.filter(email=validated_data["email"]).first()
        if not user or not user.check_password(validated_data["password"]):
            return error_response(
                message="Invalid credentials. Please check your email and password.",
                status=status.HTTP_401_UNAUTHORIZED,
            )
        if not user.is_active:
            return error_response(
                message="User is inactive. Please contact support or your administrator.",
                status=status.HTTP_403_FORBIDDEN,
            )
        login(request, user)
        user_data = UserSerializer(user).data
        return success_response(
            message="Sign in successful",
            data=user_data,
            status_code=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["get"], url_path="me")
    def me(self, request, *args, **kwargs):
        data = {"authenticated": False, "user": None}
        if request.user.is_authenticated:
            data["authenticated"] = True
            data["user"] = UserSerializer(request.user).data

        return success_response(
            data=data,
            status=status.HTTP_200_OK,
        )
