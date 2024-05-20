from django.shortcuts import render, get_object_or_404

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import (
    TaskOverviewSerializer,
    TaskDetailsSerializer,
    TaskCreateSerializer,
    CommentSerializer,
    ProjectOverviewSerializer,
    ProjectDetailsSerializer,
)
from .models import Task, Comment, Project
from django.db.models import Prefetch


class TaskViewSet(viewsets.ViewSet):
    """ViewSet for the Task model."""
    permission_classes=(AllowAny,)
    lookup_field = "uuid"

    def list(self, request):
        """Returns a list of tasks.
        
        Tasks are returned in reverse chronological order; newest to
        oldest. When listing tasks, only the UUID and summary fields
        are returned."""
        queryset = Task.objects.prefetch_related(
                Prefetch("comments", queryset=Comment.objects.order_by('-date_created'))
            ).order_by("-date_created")
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
        serializer = TaskCreateSerializer(data=request.data)
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