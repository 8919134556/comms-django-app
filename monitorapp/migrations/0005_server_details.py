# Generated by Django 4.1.4 on 2023-01-16 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitorapp', '0004_service_action'),
    ]

    operations = [
        migrations.CreateModel(
            name='Server_details',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('server_name', models.CharField(db_column='server_name', max_length=50, verbose_name='Server_name')),
                ('server_ip', models.CharField(db_column='server_ip', max_length=50, verbose_name='Server_ip')),
                ('port_num', models.BigIntegerField(db_column='port_num', verbose_name='Port_num')),
            ],
            options={
                'db_table': 'server_details',
            },
        ),
    ]
