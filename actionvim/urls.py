from django.urls import path, include, re_path
from rest_framework.routers import SimpleRouter
from django.views.generic import TemplateView

from actionvim.accounts.views import AccountViewSet

router = SimpleRouter(use_regex_path=False, trailing_slash=False)

router.register(r"accounts", AccountViewSet, basename="accounts")

urlpatterns = [
    path("api/", include(router.urls)),
    re_path(r".*", TemplateView.as_view(template_name="index.html")),
]
