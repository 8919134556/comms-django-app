# Generated by Django 4.1.4 on 2023-01-30 05:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitorapp', '0015_log_activity_login_time_log_activity_logout_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='log_activity',
            name='Action',
            field=models.CharField(blank=True, db_column='action', max_length=50, null=True, verbose_name='Action'),
        ),
        migrations.AlterField(
            model_name='log_activity',
            name='service_name',
            field=models.CharField(blank=True, db_column='service_name', max_length=50, null=True, verbose_name='Service_name'),
        ),
    ]
