from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from rest_framework import status
from django.contrib.auth import login

from actionvim.accounts.models import Account, User
from actionvim.organizations.models import Organization
from actionvim.accounts.serializers import (
    LoginSerializer,
    OrganizationSerializer,
    UserSerializer,
    RegisterSerializer,
)
from actionvim.response import success_response, error_response


class AccountsViewSet(ViewSet):

    @action(detail=False, methods=["post"], url_path="register")
    def register(self, request, *args, **kwargs):
        register_serializer = RegisterSerializer(data=request.data)
        if not register_serializer.is_valid():
            return error_response(
                errors=register_serializer.errors,
                message="Registration failed",
                status=status.HTTP_400_BAD_REQUEST,
            )

        account_data = register_serializer.validated_data
        company_name = account_data.pop("company_name", None)

        existing_account_quersey = Account.objects.filter(email=account_data["email"])
        if existing_account_quersey.exists():
            return error_response(
                message="Email already registered",
                status=status.HTTP_400_BAD_REQUEST,
            )

        account = Account.objects.create(
            email=account_data["email"],
        )
        account.set_password(account_data["password"])
        account.save()

        organization = Organization.objects.create(name=company_name)
        User.objects.create(
            email=account.email,
            account=account,
            organization=organization,
            full_name=account_data["full_name"],
            role=User.Role.OWNER,  # Assuming the first user is an admin
        )

        return success_response(
            data={"email": account.email},
            message="Account created successfully",
            status=status.HTTP_201_CREATED,
        )

    @action(detail=False, methods=["post"], url_path="login")
    def login(self, request, *args, **kwargs):
        login_serializer = LoginSerializer(data=request.data)
        if not login_serializer.is_valid():
            return error_response(
                errors=login_serializer.errors,
                message="Invalid login credentials",
                status=status.HTTP_400_BAD_REQUEST,
            )

        login_data = login_serializer.validated_data
        account = Account.objects.filter(email=login_data["email"]).first()
        if not account or not account.check_password(login_data["password"]):
            return error_response(
                message="Invalid email or password",
                status=status.HTTP_400_BAD_REQUEST,
            )

        organizations = Organization.objects.filter(users__account=account)
        organization_serializer = OrganizationSerializer(organizations, many=True)

        response_data = {
            "organizations": organization_serializer.data,
            "account": {
                "id": account.id,
                "email": account.email,
            },
            "resolve": True,
        }
        request.session["account_id"] = str(account.id)
        return success_response(
            data=response_data,
            message="Login initiated",
            status=status.HTTP_200_OK,
        )

    @action(detail=False, methods=["post"], url_path="login/resolve-user")
    def login_resolve_user(self, request, *args, **kwargs):
        organization_id = request.query_params.get("organization_id")
        account_id = request.session.get("account_id")
        if not account_id:
            return error_response(
                message="No account found in session",
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = User.objects.filter(
            account_id=account_id, organization_id=organization_id
        ).first()
        if not user:
            return error_response(
                message="User not found for the given organization",
                status=status.HTTP_404_NOT_FOUND,
            )
        login(request, user)
        user_serializer = UserSerializer(user)

        return success_response(
            data=user_serializer.data,
            message="User resolved successfully",
            status=status.HTTP_200_OK,
        )
