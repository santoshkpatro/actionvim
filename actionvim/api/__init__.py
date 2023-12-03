from django.urls import path
from .user import SignInAPIView, TokenAPIView
from .projects import ProjectListCreateAPIView, ProjectDetailAPIView

urlpatterns = [
    path("user/sign_in/", SignInAPIView.as_view(), name="api-user-sign-in"),
    path("user/token/", TokenAPIView.as_view(), name="api-user-token"),

    path("projects/", ProjectListCreateAPIView.as_view(), name="api-project-list-create"),
    path("projects/<str:public_id>/", ProjectDetailAPIView.as_view(), name="api-porject-detail")
]
