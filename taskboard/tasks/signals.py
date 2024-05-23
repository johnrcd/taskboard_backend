from django.db.models.signals import post_save
from django.db import transaction
from django.dispatch import receiver

from functools import partial

from .models import Comment, Notification, Task


@receiver(post_save, sender=Comment)
def comment_post_save_handler(sender, instance, **kwargs):
    """Creates a new Notification model whenever a comment is posted on
    a task."""

    comment_poster = instance.poster.username
    notification_receiver = instance.task.author
    task_summary = instance.task.summary

    message = str(comment_poster) + \
            " has posted a comment on your task: " + \
            str(task_summary)
    
    Notification.objects.create(
        receiver=notification_receiver,
        message=message
    )

@receiver(post_save, sender=Task)
def task_post_save_handler(sender, instance, *args, **kwargs):
    """Handles the validation of Tasks when they are saved."""
    
    # need this if statement or else it'll endlessly recurse
    if instance.type == instance.Type.PROJECT and instance.project != None:
        transaction.on_commit(partial(
            validate_task_instance,
            sender=sender,
            instance=instance,
        ))

# https://docs.djangoproject.com/en/5.0/topics/db/transactions/#performing-actions-after-commit
def validate_task_instance(sender, instance, *args, **kwargs):
    if instance.type == instance.Type.PROJECT and instance.project != None:
        print("\r\nAttempting to save Task model instance with type as " \
                "Type.PROJECT, but project field is set as not null. The " \
                "project field will be automatically set to null.\r\n"
                )
        instance.project = None
    super(Task, instance).save(*args, **kwargs)