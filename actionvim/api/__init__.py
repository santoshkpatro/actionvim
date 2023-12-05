from django.urls import path
from .user import ProfileAPIView, LoginAPIView, LogoutAPIView
from .projects import ProjectListCreateAPIView, ProjectDetailAPIView
from .sections import (
    SectionListCreateAPIView,
    SectionTaskListCreateAPIView,
    SectionArchiveAPIView,
    SectionDetailAPIView,
    SectionRestoreAPIView
)
from .tasks import TaskListCreateAPIView, TaskDetailAPIView

urlpatterns = [
    path("user/login/", LoginAPIView.as_view(), name="api-user-login"),
    path("user/profile/", ProfileAPIView.as_view(), name="api-user-profile"),
    path("user/logout/", LogoutAPIView.as_view(), name="api-user-logout"),
    # Projects API's
    path(
        "projects/", ProjectListCreateAPIView.as_view(), name="api-project-list-create"
    ),
    path(
        "projects/<str:project_public_id>/",
        ProjectDetailAPIView.as_view(),
        name="api-project-detail",
    ),
    
    ## Sections API's
    # GET, POST - /api/<>/sections/
    path(
        "projects/<str:project_public_id>/sections/",
        SectionListCreateAPIView.as_view(),
        name="api-section-list-create",
    ),

    # GET, PATCH, DELETE - /api/<>/sections/:id
    path(
        "projects/<str:project_public_id>/sections/<uuid:section_id>/",
        SectionDetailAPIView.as_view(),
        name="api-section-detail",
    ),

    # PATCH - /api/<>/sections/:id/archive/
    path(
        "projects/<str:project_public_id>/sections/<uuid:section_id>/archive/",
        SectionArchiveAPIView.as_view(),
        name="api-section-archive",
    ),

    # PATCH - /api/<>/sections/:id/restore/ 
    path(
        "projects/<str:project_public_id>/sections/<uuid:section_id>/restore/",
        SectionRestoreAPIView.as_view(),
        name="api-section-restore",
    ),

    # GET, POST - /api/<>/sections/:id/tasks/ 
    path(
        "projects/<str:project_public_id>/sections/<uuid:section_id>/tasks/",
        SectionTaskListCreateAPIView.as_view(),
        name="api-section-task-list-create",
    ),


    ## Tasks API's
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
