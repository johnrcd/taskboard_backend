from django.shortcuts import render, get_object_or_404

from rest_framework import viewsets
from rest_framework.response import Response
from .serializers import TaskOverviewSerializer, TaskDetailsSerializer
from .models import Task


# Create your views here.

class TaskViewSet(viewsets.ViewSet):
    """
    CRUD Functionality related to Tasks.
    """

    queryset = Task.objects.all()
    lookup_field = "uuid"

    def list(self, request):
        serializer = TaskOverviewSerializer(self.queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, uuid=None):
        task = get_object_or_404(self.queryset, uuid=uuid)
        serializer = TaskDetailsSerializer(task)
        return Response(serializer.data)