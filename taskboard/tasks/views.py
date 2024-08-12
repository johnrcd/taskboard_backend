from django.shortcuts import render, get_object_or_404

from rest_framework import viewsets, status
from rest_framework.decorators import api_view, schema, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from .serializers import (
    TaskOverviewSerializer,
    TaskDetailsSerializer,
    TaskCreateSerializer,
    CommentSerializer,
    CommentCreateSerializer,
    ProjectOverviewSerializer,
    ProjectDetailsSerializer,
    NotificationDetailsSerializer,
    ActivityDetailsSerializer,
)
from .models import Task, Comment, Project, Notification, Activity
from users.models import TaskboardUser
from django.db.models import Prefetch
import uuid


class TaskViewSet(viewsets.ViewSet):
    """ViewSet for the Task model."""

    permission_classes=(IsAuthenticatedOrReadOnly,)
    lookup_field = "uuid"

    def list(self, request):
        """Returns a list of tasks.
        
        Tasks are returned in reverse chronological order; newest to
        oldest. When listing tasks, only the UUID and summary fields
        are returned."""

        sort_style = "-datetime_created"

        if request.GET.get("filter", "") != "":
            pass

        # https://stackoverflow.com/a/3500905
        if request.GET.get("sort", "") != "":
            match request.GET.get("sort"):
                case "created": # default
                    sort_style = "-datetime_created"
                    pass
                case "edited":
                    sort_style = "-datetime_edited"
                case _:
                    pass # TODO: draw exception?

        queryset = Task.objects.prefetch_related(
                Prefetch("comments", queryset=Comment.objects.order_by("-date_created"))
            ).order_by(sort_style)

        serializer = TaskOverviewSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, uuid=None):
        """Returns a single task.
        
        Use a task's UUID to access it directly."""
        queryset = Task.objects.all()
        task = get_object_or_404(queryset, uuid=uuid)
        serializer = TaskDetailsSerializer(task)
        return Response(serializer.data)
    
    def create(self, request):
        data_copy = request.data.copy()

        try:
            data_copy["author"] = request.user.id
        except Exception:
            message = {
                "details" : "Attempted to create a new task, but failed to " \
                    "set author field." ,
            }
            return Response(message, status=status.HTTP_404_NOT_FOUND)
        
        try:
            project_name = data_copy["project"]
            if str(project_name) != "":
                data_copy["project"] = Project.objects.get(name=project_name).id
        except Exception:
            message = {
                "details" : "Could not find project with a name of " \
                    + str(project_name) + "."
            }
            return Response(message, status=status.HTTP_404_NOT_FOUND)

        serializer = TaskCreateSerializer(data=data_copy)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProjectViewSet(viewsets.ViewSet):
    """ViewSet for the Projects model."""

    permission_classes=(AllowAny,)
    lookup_field = "name"

    def list(self, request):
        """Returns the list of projects."""

        queryset = Project.objects.all()
        serializer = ProjectOverviewSerializer(queryset, many=True)
        project_list = []
        for item in serializer.data:
            project_list.append((item.pop("name")))
            pass
        
        return Response(project_list)
    
    def retrieve(self, request, name=None):
        """Returns a single project."""

        queryset = Project.objects.all()
        project = get_object_or_404(queryset, name=name)
        serializer = ProjectDetailsSerializer(project)
        return Response(serializer.data)


class CommentViewSet(viewsets.ViewSet):
    """ViewSet for the Comments model."""

    permission_classes=(IsAuthenticatedOrReadOnly,)

    def list(self, request):
        queryset = Comment.objects.all()
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        """Returns a single comment."""

        queryset = Comment.objects.all()
        comment = get_object_or_404(queryset, pk=pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)
    
    def create(self, request):
        data_copy = request.data.copy()

        try:
            data_copy["poster"] = request.user.id
        except Exception:
            message = {
                "details" : "Attempted to create a new comment, but failed to " \
                    "set author field." ,
            }
            return Response(message, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CommentCreateSerializer(data=data_copy)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET"])
def view_notifications(request, username):
    """Returns the user's current notifications"""

    user = get_object_or_404(TaskboardUser.objects.all(), username=username)
    queryset = Notification.objects.filter(receiver=user)
    serializer = NotificationDetailsSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def view_user_activity(request, username):
    """Returns a list of a user's activity on the website."""

    user = get_object_or_404(TaskboardUser.objects.all(), username=username)
    queryset = Activity.objects.filter(user=user).order_by("-datetime_created")
    serializer = ActivityDetailsSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(["GET"])
def get_task_types(request):
    """Returns a list of the different types a task can have."""
    return Response(Task.Type.choices)

@api_view(["GET"])
def get_task_status_types(request):
    """Returns a list of the different status values a task can
    have."""
    return Response(Task.Status.choices)

        