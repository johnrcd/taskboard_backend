# Generated by Django 5.0.3 on 2024-04-01 00:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0006_rename_poster_task_author_task_status_comment_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('summary', models.CharField(blank=True, default='No summary provided.', max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='task',
            name='project',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='tasks.project'),
        ),
    ]
