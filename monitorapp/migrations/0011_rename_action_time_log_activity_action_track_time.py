# Generated by Django 4.1.4 on 2023-01-30 05:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitorapp', '0010_alter_log_activity_action_time_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='log_activity',
            old_name='action_time',
            new_name='action_track_time',
        ),
    ]
