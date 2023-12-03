from django.urls import path
from .user import ProfileAPIView, LoginAPIView, LogoutAPIView
from .projects import ProjectListCreateAPIView, ProjectDetailAPIView
from .sections import SectionListCreateAPIView, SectionTaskListAPIView
from .tasks import TaskListCreateAPIView, TaskDetailAPIView

urlpatterns = [
    path("user/login/", LoginAPIView.as_view(), name="api-user-login"),
    path("user/profile/", ProfileAPIView.as_view(), name="api-user-profile"),
    path("user/logout/", LogoutAPIView.as_view(), name="api-user-logout"),
    path(
        "projects/", ProjectListCreateAPIView.as_view(), name="api-project-list-create"
    ),
    path(
        "projects/<str:project_public_id>/",
        ProjectDetailAPIView.as_view(),
        name="api-project-detail",
    ),
    path(
        "projects/<str:project_public_id>/sections/",
        SectionListCreateAPIView.as_view(),
        name="api-section-list-create",
    ),
    path(
        "projects/<str:project_public_id>/sections/<uuid:section_id>/tasks/",
        SectionTaskListAPIView.as_view(),
        name="api-section-tasks",
    ),
    path(
        "projects/<str:project_public_id>/tasks/",
        TaskListCreateAPIView.as_view(),
        name="api-task-list-create",
    ),
    path(
        "projects/<str:project_public_id>/tasks/<str:task_public_id>/",
        TaskDetailAPIView.as_view(),
        name="api-task-detail",
    ),
]
