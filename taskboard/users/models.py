# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator
from django.utils.translation import gettext_lazy as _

class TaskboardUser(AbstractUser):
    
    username = models.CharField(
        unique=True,
        max_length=24,
        validators=[
            MinLengthValidator(
                3, _("Minimum username length is 3 characters."),
            ),
            # NOTE: validators only work for model forms.
            #       just use serializers to produce errors
            RegexValidator(
                regex=r'[a-zA-Z0-9_-]+$',
                message=("Usernames may only have alphanumerical characters, " \
                  "underscores, and dashes.")
            )
        ],
    )
    """Usernames are restricted to a length of 3 to 24 characters."""

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username