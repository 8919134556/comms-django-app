# Generated by Django 4.1.4 on 2023-01-30 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitorapp', '0019_alter_log_activity_login_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='server_details',
            name='db_driver',
            field=models.CharField(db_column='db_driver', max_length=50, null=True, verbose_name='Db_Driver'),
        ),
        migrations.AddField(
            model_name='server_details',
            name='db_ip',
            field=models.CharField(db_column='db_ip', max_length=50, null=True, verbose_name='Db_ip'),
        ),
        migrations.AddField(
            model_name='server_details',
            name='db_name',
            field=models.CharField(db_column='db_Name', max_length=50, null=True, verbose_name='Db_name'),
        ),
        migrations.AddField(
            model_name='server_details',
            name='db_pwd',
            field=models.CharField(db_column='db_pwd', max_length=50, null=True, verbose_name='Db_pwd'),
        ),
        migrations.AddField(
            model_name='server_details',
            name='db_user_name',
            field=models.CharField(db_column='db_user_name', max_length=50, null=True, verbose_name='Db_user_name'),
        ),
        migrations.AlterField(
            model_name='server_details',
            name='port_num',
            field=models.BigIntegerField(db_column='port_num', null=True, verbose_name='Port_num'),
        ),
        migrations.AlterField(
            model_name='server_details',
            name='server_ip',
            field=models.CharField(db_column='server_ip', max_length=50, null=True, verbose_name='Server_ip'),
        ),
        migrations.AlterField(
            model_name='server_details',
            name='server_name',
            field=models.CharField(db_column='server_name', max_length=50, null=True, verbose_name='Server_name'),
        ),
    ]
