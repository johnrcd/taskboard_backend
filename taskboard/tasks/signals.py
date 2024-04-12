from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Comment, Notification


@receiver(post_save, sender=Comment)
def SendNotificationOnCommentPost(sender, instance, **kwargs):
    comment_poster = instance.poster.username
    notification_receiver = instance.task.author
    task_summary = instance.task.summary

    message = str(comment_poster) + " has posted a comment on your task: " + \
            str(task_summary)
    
    Notification.objects.create(
        receiver=notification_receiver,
        message=message
    )