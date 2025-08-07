import pytest
from django.db import IntegrityError
from actionvim.accounts.models import Account, User
from actionvim.organizations.models import Organization


@pytest.fixture
def org():
    return Organization.objects.create(name="Acme Inc.")


@pytest.fixture
def account():
    return Account.objects.create(email="user@example.com")


@pytest.mark.django_db
def test_user_code_auto_generated(account, org):
    user = User.objects.create(
        email="user@example.com",
        full_name="Test User",
        account=account,
        organization=org,
    )
    assert user.user_code
    assert len(user.user_code) == 12


@pytest.mark.django_db
def test_default_role_is_staff(account, org):
    user = User.objects.create(
        email="user@example.com",
        full_name="Test User",
        account=account,
        organization=org,
    )
    assert user.role == User.Role.STAFF


@pytest.mark.django_db
def test_user_email_unique_per_org(account, org):
    User.objects.create(
        email="duplicate@example.com",
        full_name="User One",
        account=account,
        organization=org,
    )
    with pytest.raises(IntegrityError):
        User.objects.create(
            email="duplicate@example.com",
            full_name="User Two",
            account=account,
            organization=org,
        )


@pytest.mark.django_db
def test_same_email_allowed_different_org(account, org):
    other_org = Organization.objects.create(name="Another Org")

    User.objects.create(
        email="shared@example.com",
        full_name="User One",
        account=account,
        organization=org,
    )

    user2 = User.objects.create(
        email="shared@example.com",
        full_name="User Two",
        account=account,
        organization=other_org,
    )

    assert user2.organization == other_org
