# Generated by Django 5.0.3 on 2024-08-11 01:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0024_activity_datetime_created'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='datetime_edited',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
