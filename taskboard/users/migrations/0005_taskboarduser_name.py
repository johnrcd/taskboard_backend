# Generated by Django 5.0.3 on 2024-06-28 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_taskboarduser_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskboarduser',
            name='name',
            field=models.CharField(blank=True, default='', max_length=127),
        ),
    ]
