# Generated by Django 5.0.3 on 2024-04-11 02:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0016_alter_task_author_alter_task_description_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='comments',
        ),
        migrations.AddField(
            model_name='comment',
            name='task',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='tasks.task'),
            preserve_default=False,
        ),
    ]
