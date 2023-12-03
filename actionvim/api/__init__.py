from django.urls import path
from .user import TokenAPIView, ProfileAPIView, LoginAPIView, LogoutAPIView
from .projects import ProjectListCreateAPIView, ProjectDetailAPIView
from .sections import SectionListCreateAPIView

urlpatterns = [
    path("user/login/", LoginAPIView.as_view(), name="api-user-login"),
    path("user/token/", TokenAPIView.as_view(), name="api-user-token"),
    path("user/profile/", ProfileAPIView.as_view(), name="api-user-profile"),
    path("user/logout/", LogoutAPIView.as_view(), name="api-user-logout"),

    path("projects/", ProjectListCreateAPIView.as_view(), name="api-project-list-create"),
    path("projects/<str:public_id>/", ProjectDetailAPIView.as_view(), name="api-project-detail"),
    path("projects/<str:public_id>/sections/", SectionListCreateAPIView.as_view(), name="api-section-list-create")
]
