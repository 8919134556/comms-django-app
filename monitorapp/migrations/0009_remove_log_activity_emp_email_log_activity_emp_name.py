# Generated by Django 4.1.4 on 2023-01-30 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitorapp', '0008_alter_log_activity_table'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='log_activity',
            name='emp_email',
        ),
        migrations.AddField(
            model_name='log_activity',
            name='emp_name',
            field=models.CharField(blank=True, db_column='emp_name', max_length=100, null=True, verbose_name='Emp_Name'),
        ),
    ]
