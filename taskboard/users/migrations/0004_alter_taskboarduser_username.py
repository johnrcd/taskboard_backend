# Generated by Django 5.0.3 on 2024-06-16 02:02

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_taskboarduser_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskboarduser',
            name='username',
            field=models.CharField(max_length=24, unique=True, validators=[django.core.validators.MinLengthValidator(3, 'Minimum username length is 3 characters.'), django.core.validators.RegexValidator(message='Usernames may only have alphanumerical characters, underscores, and dashes.', regex='[a-zA-Z0-9_-]+$')]),
        ),
    ]
