# Generated by Django 5.0.3 on 2024-08-11 01:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0025_task_datetime_edited'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ['-datetime_created']},
        ),
        migrations.RenameField(
            model_name='task',
            old_name='date_created',
            new_name='datetime_created',
        ),
    ]
