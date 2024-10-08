from rest_framework import serializers
from django.shortcuts import get_object_or_404
from .models import TaskboardUser
from rest_framework.exceptions import ValidationError
import re

class TaskboardUserCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a comment."""

    class Meta:
        model = TaskboardUser
        fields = "__all__"

    def create(self, validated_data):
        """Creates a new comment."""
        
        message = {
            "username": ["Usernames may only have alphanumerical " \
                "characters, underscores, and dashes.", ]
        }
        if not re.fullmatch(r'[a-zA-Z0-9_-]+$', validated_data["username"]):
            raise ValidationError(message)

        user = TaskboardUser.objects.create_user(
            username=validated_data["username"],
        )

        user.set_password(validated_data["password"])
        user.save()
        
        return user

class TaskboardUserProfileSerializer(serializers.ModelSerializer):
    """Serializer for viewing a user's profile."""

    class Meta:
        model = TaskboardUser
        fields = (
            "username",
            "name",
            "title",
            "about_me",
        )

class TaskboardUserModificationSerializer(serializers.ModelSerializer):
    """serializer for making changes for a Taskboard User."""
    class Meta:
        model = TaskboardUser
        fields = "__all__"