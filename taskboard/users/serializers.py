from rest_framework import serializers
from django.shortcuts import get_object_or_404
from .models import TaskboardUser

class TaskboardUserCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a comment."""

    class Meta:
        model = TaskboardUser
        fields = "__all__"

    def create(self, validated_data):
        """Creates a new comment."""
        
        user = TaskboardUser.objects.create_user(
            username=validated_data["username"],
        )

        user.set_password(validated_data["password"])
        user.save()
        
        return user
