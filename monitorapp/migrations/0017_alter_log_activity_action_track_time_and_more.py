# Generated by Django 4.1.4 on 2023-01-30 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitorapp', '0016_alter_log_activity_action_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log_activity',
            name='action_track_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='log_activity',
            name='login_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='log_activity',
            name='logout_time',
            field=models.DateTimeField(null=True),
        ),
    ]