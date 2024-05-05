from django.shortcuts import render, get_object_or_404

from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import (
    TaskOverviewSerializer,
    TaskDetailsSerializer,
    CommentSerializer,
)
from .models import Task, Comment
from django.db.models import Prefetch


class TaskViewSet(viewsets.ViewSet):
    """ViewSet for the Task model."""

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