from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

class Task(models.Model):
    class Category(models.TextChoices):
        NONE          = "NONE", _("None")
        GAMES         = "GAME", _("Games")
        WEBSITES      = "SITE", _("Websites")
        APPS          = "APPS", _("Apps")
        MISCELLANEOUS = "MISC", _("Miscellaneous")

    class Type(models.TextChoices):
        NONE     = "NONE", _("None"),
        CONCEPT  = "CNPT", _("Concept")
        IDEA     = "IDEA", _("Idea")
        ISSUE    = "ISSU", _("Issue")
        UNSORTED = "UNST", _("Unsorted")

    class Status(models.TextChoices):
        TODO        = 'TODO', _("To Do")
        REJECTED    = 'NOPE', _("Rejected")
        CANCELLED   = 'STOP', _("Cancelled")
        IN_PROGRESS = 'WORK', _("In Progress")
        REVIEWING   = 'REVW', _("Reviewing")
        COMPLETE    = 'DONE', _("Complete")

    title = models.CharField(
        max_length=200,
        blank=True,
        default="No title provided.",
    )

    description = models.CharField(
        max_length=1000,
        blank=True,
        default="No description provided."
    )

    poster = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )

    category = models.CharField(
        max_length=4,
        choices=Category,
        default=Category.NONE,
    )

    type = models.CharField(
        max_length=4,
        choices=Type,
        default=Type.NONE,
    )

    status = models.CharField(
        max_length=4,
        choices=Status,
        default=Status.TODO,
    )