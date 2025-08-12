from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.conf import settings
from django.shortcuts import render
from django.http import FileResponse
from rest_framework.routers import SimpleRouter


def index(request):
    index_path = settings.BASE_DIR / "frontend" / "index.html"
    if settings.DEBUG:
        return render(request, "index.html")

    return FileResponse(open(index_path, "rb"), content_type="text/html")


from actionvim.accounts.views import AccountViewSet

router = SimpleRouter(use_regex_path=False, trailing_slash=False)

router.register(r"accounts", AccountViewSet, basename="accounts")

urlpatterns = [
    path("api/", include(router.urls)),
    re_path(r".*", index, name="index"),
]
