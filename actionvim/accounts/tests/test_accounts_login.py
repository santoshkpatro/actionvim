import pytest
from rest_framework.test import APIClient
from actionvim.accounts.models import Account, User
from actionvim.organizations.models import Organization


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def account(db):
    acc = Account.objects.create(email="user@example.com")
    acc.set_password("testpass123")
    acc.save()
    return acc


@pytest.fixture
def organization(db):
    return Organization.objects.create(name="Test Org")


@pytest.fixture
def user(db, account, organization):
    return User.objects.create(
        email="user@example.com",
        account=account,
        organization=organization,
        full_name="Test User",
        role=User.Role.STAFF,
    )


@pytest.mark.django_db
def test_login_step1_success(api_client, account, user, organization):
    url = "/api/accounts/login"  # no trailing slash
    payload = {"email": "user@example.com", "password": "testpass123"}

    response = api_client.post(url, data=payload)
    assert response.status_code == 200
    assert response.data["success"] is True
    assert response.data["data"]["account"]["email"] == "user@example.com"
    assert "organizations" in response.data["data"]


@pytest.mark.django_db
def test_login_step1_invalid_credentials(api_client):
    url = "/api/accounts/login"
    payload = {"email": "nonexistent@example.com", "password": "wrongpass"}

    response = api_client.post(url, data=payload)
    assert response.status_code == 400
    assert response.data["success"] is False


@pytest.mark.django_db
def test_login_resolve_user_success(api_client, account, user, organization):
    # Step 1: simulate login and session
    api_client.post(
        "/api/accounts/login",
        data={"email": "user@example.com", "password": "testpass123"},
    )

    # Step 2: resolve user by org
    response = api_client.post(
        "/api/accounts/login/resolve-user",
        data={},
        QUERY_STRING=f"organization_id={organization.id}",
    )

    assert response.status_code == 200
    assert response.data["success"] is True
    assert response.data["data"]["email"] == "user@example.com"


@pytest.mark.django_db
def test_login_resolve_user_no_session(api_client, organization):
    response = api_client.post(
        "/api/accounts/login/resolve-user",
        data={},
        QUERY_STRING=f"organization_id={organization.id}",
    )

    assert response.status_code == 400
    assert response.data["success"] is False
    assert response.data["message"] == "No account found in session"
