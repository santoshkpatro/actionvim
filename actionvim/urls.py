from django.urls import path, include, re_path
from django.conf import settings
from django.shortcuts import render
from django.http import FileResponse
from rest_framework.routers import SimpleRouter

from actionvim.shared.views import SiteMetaView
from actionvim.accounts.views import AccountViewSet


def index(request):
    index_path = settings.BASE_DIR / "frontend" / "index.html"
    if settings.DEBUG:
        return render(request, "index.html")

    return FileResponse(open(index_path, "rb"), content_type="text/html")


router = SimpleRouter(use_regex_path=False, trailing_slash=False)
router.register(r"accounts", AccountViewSet, basename="accounts")

urlpatterns = [
    path("api/", include(router.urls)),
    path("api/site-meta", SiteMetaView.as_view(), name="site-meta"),
    re_path(r".*", index, name="index"),
]
