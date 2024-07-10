from rest_framework import serializers
from django.shortcuts import get_object_or_404
from .models import Task, Project, Comment, Notification
from users.models import TaskboardUser

class TaskOverviewSerializer(serializers.ModelSerializer):
    """Returns the UUID and Summary of a task.
    
    Intended to be used when returning a list of tasks, rather than
    returning all the data.
    """
    class Meta:
        model = Task
        fields = (
            "uuid",
            "summary",
            "type",
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)

        # change summary to include type
        summary = data.pop("summary")
        type = data.pop("type")

        data.update({
            "summary": "[" + str(instance.get_type_display()) + "] " + summary
        })

        return data


class CommentSerializer(serializers.ModelSerializer):
    """Returns details of a comment.
    
    Due to the simplicity of the Comment model, there is no divide
    between the list and retrieve views. They both return the same
    fields."""
    
    class Meta:
        model = Comment
        fields = ("content", "date_created", "poster")

    def to_representation(self, instance):
        data = super().to_representation(instance)

        # replace foreign keys with string representation

        poster_pk = data.pop("poster")

        data.update({
            "poster": TaskboardUser.objects.get(pk=poster_pk).username
        })

        return data

class CommentCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a comment."""

    class Meta:
        model = Comment
        fields = "__all__"

    def create(self, validated_data):
        """Creates a new comment."""
        
        return Comment.objects.create(**validated_data)

class TaskDetailsSerializer(serializers.ModelSerializer):
    """Returns the full information regarding a task.
    
    Author and Project foreign keys are replaced with their string
    representations. Type and Status enums are replaced with their
    display strings. Comments are given as an array.
    """

    comments = CommentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Task
        fields = (
            "uuid",
            "summary",
            "description",
            "type",
            "status",
            "date_created",
            "author",
            "project",
            "comments",
        )

    def to_representation(self, instance):
        data = super().to_representation(instance)

        # replace foreign keys with string representation

        author_pk = data.pop("author")
        project_pk = data.pop("project")

        data.update({
            "author": TaskboardUser.objects.get(pk=author_pk).username}
        )

        # TODO: replace this with something that doesn't require a try/catch
        #       not sure how efficient try/catch is in Python but it can't be good lol
        try:
            project_name = "None" if instance.get_type_display() == "Project" else Project.objects.get(pk=project_pk).name
        except Exception:
            project_name = "None"

        data.update({"project": project_name})

        # replace enums with display values
        # NOTE: get_[field]_display methods autogenerated when using an
        # enum field. or maybe it's choices idk

        data.update({"type": instance.get_type_display()})
        data.update({"status": instance.get_status_display()})

        return data

class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"

    def create(self, validated_data):
        """
        Create and return a new Task instance, given the validated data.
        """ 
        return Task.objects.create(**validated_data)

class ProjectOverviewSerializer(serializers.ModelSerializer):
    """Returns project names."""

    class Meta:
        model = Project
        fields = ("name", )

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return data
    
class ProjectDetailsSerializer(serializers.ModelSerializer):
    """Returns all fields of a project model."""

    class Meta:
        model = Project
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.update({"type": instance.get_type_display()})
        return data
    
class NotificationDetailsSerializer(serializers.ModelSerializer):
    """Serializer for viewing notifications."""

    class Meta:
        model = Notification
        fields = ("message", "datetime_created", "type", "location")
