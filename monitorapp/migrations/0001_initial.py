# Generated by Django 4.1.4 on 2023-01-02 07:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comms_user',
            fields=[
                ('assign_id', models.AutoField(primary_key=True, serialize=False)),
                ('emp_name', models.CharField(db_column='Emp_name', max_length=50, verbose_name='Emp_Name')),
                ('emp_id', models.CharField(db_column='emp_id', max_length=50, null=True, verbose_name='Emp_Id')),
                ('emp_email', models.EmailField(blank=True, db_column='emp_email', max_length=100, null=True, verbose_name='Emp_Email')),
                ('emp_pwd', models.CharField(db_column='emp_pwd', max_length=100, verbose_name='Emp_Password')),
                ('emp_gender', models.CharField(db_column='emp_gender', max_length=50, verbose_name='Emp_Gender')),
                ('datetime_created', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
                'db_table': 'comms_user',
            },
        ),
    ]
