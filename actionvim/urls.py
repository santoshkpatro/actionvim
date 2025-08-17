from django.urls import path, include, re_path
from rest_framework.routers import SimpleRouter

from actionvim.misc_views import index, sign_out, health
from actionvim.shared.views import SiteMetaView
from actionvim.accounts.views import AccountViewSet
from actionvim.applications.views import AplicationViewSet

router = SimpleRouter(use_regex_path=False, trailing_slash=False)
router.register(r"accounts", AccountViewSet, basename="accounts")
router.register(r"applications", AplicationViewSet, basename="applications")

urlpatterns = [
    path("api/", include(router.urls)),
    path("api/site-meta", SiteMetaView.as_view(), name="site-meta"),
    path("sign-out", sign_out, name="sign-out"),
    path("health", health, name="health"),
    re_path(r".*", index, name="index"),
]
