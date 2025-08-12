from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.conf import settings
from django.shortcuts import render
from rest_framework.routers import SimpleRouter


def index(request):
    if settings.DEBUG:
        return render(request, "index_dev.html")
    else:
        return render(request, "index.html", status=404)


from actionvim.accounts.views import AccountViewSet

router = SimpleRouter(use_regex_path=False, trailing_slash=False)

router.register(r"accounts", AccountViewSet, basename="accounts")

urlpatterns = [
    path("api/", include(router.urls)),
    re_path(r".*", index, name="index"),
]
