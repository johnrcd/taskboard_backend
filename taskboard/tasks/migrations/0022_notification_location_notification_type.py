# Generated by Django 5.0.3 on 2024-07-10 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0021_alter_task_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='location',
            field=models.CharField(blank=True, default='', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='notification',
            name='type',
            field=models.CharField(choices=[('MSG', 'Message'), ('TSK', 'Task')], default='MSG', max_length=4),
        ),
    ]