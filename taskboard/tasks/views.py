from django.shortcuts import render, get_object_or_404

from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import (
    TaskOverviewSerializer,
    TaskDetailsSerializer,
    CommentSerializer
)
from .models import Task, Comment


# Create your views here.

class TaskViewSet(viewsets.ViewSet):
    """
    CRUD Functionality related to Tasks.
    """

    lookup_field = "uuid"

    def list(self, request):
        queryset = Task.objects.all().order_by("-date_created")
        serializer = TaskOverviewSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, uuid=None):
        queryset = Task.objects.all()
        task = get_object_or_404(queryset, uuid=uuid)
        serializer = TaskDetailsSerializer(task)
        return Response(serializer.data)
    
class CommentViewSet(viewsets.ViewSet):

    def list(self, request):
        queryset = Comment.objects.all().order_by("-date_created")
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, uuid=None):
        queryset = Comment.objects.all()
        comment = get_object_or_404(queryset, uuid=uuid)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)