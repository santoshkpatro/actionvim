import pytest
from django.contrib.auth.hashers import check_password
from actionvim.accounts.models import Account


@pytest.mark.django_db
def test_set_and_check_password():
    account = Account.objects.create(email="account@example.com")
    account.set_password("secure123")
    account.save()

    assert account.check_password("secure123")
    assert not account.check_password("wrongpass")
    assert check_password("secure123", account.password)


@pytest.mark.django_db
def test_set_unusable_password():
    account = Account.objects.create(email="account@example.com")
    account.set_unusable_password()
    account.save()

    assert not account.has_usable_password()
