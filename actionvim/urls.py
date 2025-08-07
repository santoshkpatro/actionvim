from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter

from actionvim.accounts.views import AccountsViewSet

router = SimpleRouter(use_regex_path=False, trailing_slash=False)

router.register(r"accounts", AccountsViewSet, basename="accounts")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
]
