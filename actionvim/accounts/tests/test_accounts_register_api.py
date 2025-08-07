import pytest
from rest_framework.test import APIClient
from actionvim.accounts.models import Account, User
from actionvim.organizations.models import Organization


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_register_success(api_client):
    url = "/api/accounts/register"
    payload = {
        "email": "newuser@example.com",
        "password": "strongpassword123",
        "company_name": "TestOrg Ltd",
        "confirm_password": "strongpassword123",
        "full_name": "New User",
    }

    response = api_client.post(url, data=payload)
    assert response.status_code == 201
    assert response.data["success"] is True

    account = Account.objects.get(email="newuser@example.com")
    assert account.check_password("strongpassword123")

    organization = Organization.objects.get(name="TestOrg Ltd")
    user = User.objects.get(account=account, organization=organization)

    assert user.role == User.Role.OWNER
    assert user.email == "newuser@example.com"


@pytest.mark.django_db
def test_register_duplicate_email(api_client):
    # Pre-create account with same email
    account = Account.objects.create(email="duplicate@example.com")
    account.set_password("existingpass")
    account.save()

    url = "/api/accounts/register"
    payload = {
        "email": "duplicate@example.com",
        "password": "anotherpass",
        "confirm_password": "anotherpass",
        "company_name": "DupOrg",
        "full_name": "Duplicate User",
    }

    response = api_client.post(url, data=payload)
    assert response.status_code == 400
    assert response.data["success"] is False
