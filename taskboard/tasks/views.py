from django.shortcuts import render, get_object_or_404

from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import (
    TaskOverviewSerializer,
    TaskDetailsSerializer,
    CommentSerializer,
)
from .models import Task, Comment


class TaskViewSet(viewsets.ViewSet):
    """ViewSet for the Task model."""

    lookup_field = "uuid"

    def list(self, request):
        """Returns a list of tasks.
        
        Tasks are returned in reverse chronological order; newest to
        oldest. When listing tasks, only the UUID and summary fields
        are returned."""
        queryset = Task.objects.all().order_by("-date_created")
        serializer = TaskOverviewSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, uuid=None):
        """Returns a single task.
        
        Use a task's UUID to access it directly."""
        queryset = Task.objects.all()
        task = get_object_or_404(queryset, uuid=uuid)
        serializer = TaskDetailsSerializer(task)
        return Response(serializer.data)


class CommentViewSet(viewsets.ViewSet):
    """ViewSet for the Comment model."""

    def list(self, request):
        """Returns a list of comments.
        
        Query parameter "uuid" representing a task's uuid should be
        used to limit comments returned to relate to a particular
        post.
        """

        queryset = Comment.objects.all().order_by("-date_created")

        # ref: https://www.django-rest-framework.org/api-guide/filtering/#filtering-against-query-parameters
        uuid = self.request.query_params.get('uuid')
        if uuid is not None:
            queryset = queryset.filter(task__uuid=uuid) # untested
        
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        """Returns a single comment.
        
        Use a comment's primary key to access it directly."""
        queryset = Comment.objects.all()
        comment = get_object_or_404(queryset, pk=pk)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)