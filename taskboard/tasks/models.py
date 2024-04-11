import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model


class Project(models.Model):
    """A project is an existing application.
    
    Tasks which themselves aren't suggestions for new projects will be
    connected to an existing project."""
    
    class Type(models.TextChoices):
        """Enumeration for the different project types."""

        GAME = "GAME", _("Game"),
        """Videogame.
        
        This project type takes presedence over all the other types.
        """

        MUSIC = "MSIC", _("Music"),
        """Music, whether in the form of a single song, or a
        collection.
        
        Music is chosen when the work Rovi does for the project is
        focused on music. Even when the project itself isn't music
        focused (e.g., a game), if a large majority of the work he
        does for the project is music focused, it will be categorized
        as a Music project.
        """

        WEBSITE = "SITE", _("Website"),
        """Website.
        
        When a project can be considered a "webapp" (accessable
        through both an execuable and on a web browser), the Website
        project type will take precedence.
        """

        APPLICATION = "APPL", _("Application"),
        """Standalone application. Applies to any device; computers,
        mobile devices, etc."""

        OTHER = "OTHR", _("Other"),
        """Used for projects that cannot fit neatly into one of the
        other categories."""

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

    type = models.CharField(
        max_length=4,
        choices=Type,
        default=Type.OTHER,
    )
    """Type of task."""

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

    description = models.TextField(
        # 256 * 16 - 1 because i am not doing Jira's 32,767 characters
        max_length=4095,
        blank=True,
        default=None,
    )
    """Long description of a task. If the task is an issue, this will
    explain the details of the problem; if it's a feature, it'll go
    into what the feature entails."""

    author = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="tasks",
    )
    """The user that created the task."""

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="tasks",
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

    date_created = models.DateTimeField(
        auto_now_add=True
    )
    """Date task was created."""

    def __str__(self):
        return self.summary


class Comment(models.Model):
    """Comment on a task."""

    poster = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="comments",
    )
    """The user that created the comment."""

    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="comments",
    )

    content = models.TextField(
        max_length=280, # length of a tweet lol
        blank=True,
        default=None,
    )
    """Content of the comment."""

    date_created = models.DateTimeField(
        auto_now_add=True
    )
    """Datetime that comment was created."""
    
    def __str__(self):
        return str(self.poster) + ": " + str(self.content)