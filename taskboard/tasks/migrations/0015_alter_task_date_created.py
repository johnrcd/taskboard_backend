# Generated by Django 5.0.3 on 2024-04-10 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0014_rename_status_comment_task_comments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]