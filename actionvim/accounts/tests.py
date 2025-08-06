from django.test import TestCase
from django.contrib.auth.hashers import check_password
from django.db.utils import IntegrityError

from actionvim.accounts.models import Account, User
from actionvim.organizations.models import Organization


class AccountPasswordTests(TestCase):
    def setUp(self):
        self.account = Account.objects.create(email="account@example.com")

    def test_set_and_check_password(self):
        self.account.set_password("secure123")
        self.account.save()

        self.assertTrue(self.account.check_password("secure123"))
        self.assertFalse(self.account.check_password("wrongpass"))
        self.assertTrue(check_password("secure123", self.account.password))

    def test_set_unusable_password(self):
        self.account.set_unusable_password()
        self.account.save()

        self.assertFalse(self.account.has_usable_password())


class UserTests(TestCase):
    def setUp(self):
        self.org = Organization.objects.create(name="Acme Inc.")
        self.account = Account.objects.create(email="user@example.com")

    def test_user_code_auto_generated(self):
        user = User.objects.create(
            email="user@example.com",
            full_name="Test User",
            account=self.account,
            organization=self.org,
        )
        self.assertTrue(user.user_code)
        self.assertEqual(len(user.user_code), 12)

    def test_default_role_is_staff(self):
        user = User.objects.create(
            email="user@example.com",
            full_name="Test User",
            account=self.account,
            organization=self.org,
        )
        self.assertEqual(user.role, User.Role.STAFF)

    def test_user_email_unique_per_org(self):
        User.objects.create(
            email="duplicate@example.com",
            full_name="User One",
            account=self.account,
            organization=self.org,
        )
        with self.assertRaises(IntegrityError):
            User.objects.create(
                email="duplicate@example.com",
                full_name="User Two",
                account=self.account,
                organization=self.org,
            )

    def test_same_email_allowed_different_org(self):
        other_org = Organization.objects.create(name="Another Org")
        User.objects.create(
            email="shared@example.com",
            full_name="User One",
            account=self.account,
            organization=self.org,
        )
        user2 = User.objects.create(
            email="shared@example.com",
            full_name="User Two",
            account=self.account,
            organization=other_org,
        )
        self.assertEqual(user2.organization, other_org)
