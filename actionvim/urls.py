from django.contrib import admin
from django.urls import path, re_path, include
from .views import IndexView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("actionvim.api")),
    re_path("^(.*)$", IndexView.as_view(), name="index")
]
