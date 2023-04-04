from django.db import models
from datetime import datetime
from django.utils.timezone import get_current_timezone
# Create your models here.
class Comms_user(models.Model):
    pri_id = models.AutoField(primary_key=True)

    emp_name = models.CharField(verbose_name='Emp_Name', db_column="emp_name", max_length=50, blank=False,
                                  null=False)
    
    emp_email = models.EmailField(db_column='emp_email', verbose_name='Emp_Email', max_length=100, null=True, blank=True)

    emp_pwd=models.CharField(verbose_name='Emp_Password',db_column="emp_pwd",max_length=100,blank=False,null=False)
    
    emp_gender=models.CharField(verbose_name='Emp_Gender',db_column="emp_gender",max_length=50,blank=False,null=False)

    emp_role=models.CharField(verbose_name='Emp_Role',db_column="emp_role",max_length=50,blank=False,null=True)
    
    server_name=models.CharField(verbose_name='Server_name',db_column="server_name",max_length=50,blank=False,null=True)
    datetime_created = models.DateTimeField(default=datetime.now)
    
    class Meta:
        db_table='comms_user'

class log_activity(models.Model):
    pri_id = models.AutoField(primary_key=True)
    emp_name = models.CharField(db_column='emp_name', verbose_name='Emp_Name', max_length=100, null=True, blank=True)
    service_name = models.CharField(verbose_name='Service_name', db_column="service_name", max_length=50, blank=True,null=True)
    Action = models.CharField(verbose_name='Action', db_column="action", max_length=50, blank=True,null=True)
    action_track_time = models.CharField(db_column='action_track_time', verbose_name='Action_Track_Time', max_length=100, null=True, blank=True)
    login_time = models.CharField(db_column='login_time', verbose_name='Login_Time', max_length=100, null=True, blank=True)
    logout_time = models.CharField(db_column='logout_time', verbose_name='Logout_Time', max_length=100, null=True, blank=True)

    class Meta:
        db_table='log_activity'


class Server_details(models.Model):
    id = models.AutoField(primary_key=True)
    server_name = models.CharField(verbose_name='Server_name', db_column="server_name", max_length=50, blank=False,
                                  null=True)
    server_ip = models.CharField(verbose_name='Server_ip', db_column="server_ip", max_length=50, blank=False,
                                  null=True)
    port_num = models.BigIntegerField(verbose_name='Port_num', db_column="port_num", blank=False,
                                  null=True)
    db_driver = models.CharField(verbose_name='Db_Driver', db_column="db_driver", max_length=50, blank=False,
                                  null=True)
    db_ip = models.CharField(verbose_name='Db_ip', db_column="db_ip", max_length=50, blank=False,
                                  null=True)
    db_user_name = models.CharField(verbose_name='Db_user_name', db_column="db_user_name", max_length=50, blank=False,
                                  null=True)
    db_pwd = models.CharField(verbose_name='Db_pwd', db_column="db_pwd", max_length=50, blank=False,
                                  null=True)
    db_name = models.CharField(verbose_name='Db_name', db_column="db_Name", max_length=50, blank=False,
                                  null=True)
    db_port_num = models.BigIntegerField(verbose_name='Db_Port_num', db_column="db_port_num", blank=False,
                                  null=True)
    class Meta:
        db_table='server_details'


