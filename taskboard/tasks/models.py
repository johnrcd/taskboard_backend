import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model


class Project(models.Model):
    """A project is an existing application.
    
    Tasks which themselves aren't suggestions for new projects will be
    connected to an existing project."""

    name = models.CharField(
        max_length=255,
        unique=True,
    )
    """The name of the project."""

    summary = models.CharField(
        max_length=255,
        blank=True,
        default=None,
    )
    """An overview of a project."""

    def __str__(self):
        return self.name


class Task(models.Model):
    """A task is work that needs to be done.
    
    In the context of the Taskboard, a task is a job for Rovi to look
    into and perform.
    """
    class Type(models.TextChoices):
        """Enumeration for task types."""

        TASK    = "TASK", _("Task"),
        """Represents any task. Can be used as a default if no task
        fits, or the author is unsure of what task type to use."""

        FEATURE = "FEAT", _("Feature"),
        """Feature request for an existing project."""

        PROJECT = "PROJ", _("Project")
        """Idea for a new project."""

        ISSUE   = "ISSU", _("Issue")
        """Bug or issue with existing project."""

    class Status(models.TextChoices):
        """Enumeration for the status of a task."""

        TODO        = 'TODO', _("To Do")
        """Default value. Task is part of to do list."""

        IN_PROGRESS = 'WORK', _("In Progress")
        """Task is being worked on."""

        REVIEWING   = 'REVW', _("Reviewing")
        """Task is considered complete, but needs to be reviewed."""

        COMPLETE    = 'DONE', _("Complete")
        """Task is complete."""

        REJECTED    = 'NOPE', _("Rejected")
        """Task has been rejected.
        
        Used when a task is not deemed suitable to be on the
        taskboard. Possible reasons for rejection include:

        - Not enough information,
        - Impossible to do,
        - or duplicate of another task.
        """

        CANCELLED   = 'STOP', _("Cancelled")
        """Task has been cancelled, and cannot be completed.
        
        This status is used when an attempt to complete the task has
        been made, but it cannot or will not be completed.
        """

    class Meta:
        ordering = ['-date_created']

    uuid = models.UUIDField( 
        primary_key = True, 
        default = uuid.uuid4, 
        editable = False
    )
    """ID for a task."""
    
    summary = models.CharField(
        max_length=255, # same length as Jira summary length
        blank=True,
        default=None,
    )
    """Short description of task. Ideally a single sentence."""

    description = models.CharField(
        # 255 * 16 because i am not doing Jira's 32,767 characters
        max_length=4080,
        blank=True,
        default=None,
    )
    """Long description of a task. If the task is an issue, this will
    explain the details of the problem; if it's a feature, it'll go
    into what the feature entails."""

    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
    """The user that created the task."""

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        blank=True,
        default=None,
    )
    """The project that a task is connected to.
    
    This should always be null if the task type is Project, or at
    least treated as null.
    """

    type = models.CharField(
        max_length=4,
        choices=Type,
        default=Type.TASK,
    )
    """Type of task."""

    status = models.CharField(
        max_length=4,
        choices=Status,
        default=Status.TODO,
    )
    """Progress of task."""

    status_comment = models.CharField(
        max_length=255,
        blank=True,
        default=None,
    )
    """Optional field for explaining the reason for a status.
    
    Expected to be used for status's that are typically the final
    status for a task: Complete, Rejected, and Cancelled.
    """

    date_created = models.DateField(
        auto_now_add=True
    )
    """Date task was created."""

    def __str__(self):
        return self.summary