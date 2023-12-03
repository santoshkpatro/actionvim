from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework_simplejwt.tokens import RefreshToken
from actionvim.models import User
from rest_framework.views import APIView



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class BasicProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "username", "avatar", "phone", "tokens"]


class SignInAPIView(APIView):
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
        return Response(
            data={
                "detail": "Login success",
                "user": profile_serializer.data,
            },
            status=status.HTTP_200_OK,
        )
    

class TokenAPIView(APIView):
    def post(self, request):
        refresh_token = request.data.get("token")
        try:
            token = RefreshToken(refresh_token)
            user = User.objects.filter(id=token["user_id"]).first()
            profile_serializer = BasicProfileSerializer(user)
            return Response(data=profile_serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(data={"detail": "Token has been expired or invalid"}, status=status.HTTP_308_PERMANENT_REDIRECT)
