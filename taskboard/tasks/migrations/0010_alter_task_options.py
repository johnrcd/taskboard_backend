# Generated by Django 5.0.3 on 2024-04-04 23:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0009_remove_task_id_task_uuid'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ['-date_created']},
        ),
    ]