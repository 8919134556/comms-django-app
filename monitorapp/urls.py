from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views 

urlpatterns = [
   
   
    path('', views.login_page, name='login_page'),
    path('forgot-password', views.forgot_password, name='forgot_password'),
    # -------------------------Admin-----------------------------------------------------------
    path('admin-dashboard', views.admin_dashboard, name='admin_dashboard'),
    path('view-service', views.view_service, name='view_service'),
    path('add-user', views.add_user, name='add_user'),
    path('view-user', views.view_user, name='view_user'),
    path('logout', views.logout, name='logout'),
    # -------------------------sub-admin--------------------------------------------------------
    path('sub-admin/<str:name>', views.sub_admin, name='sub_admin'),
    path('sub-admin-updater/<str:name>', views.sub_admin_updater, name='sub_admin_updater'),
    path('sub-admin-sql-job/<str:name>', views.sub_admin_sql_job, name='sub_admin_sql_job'),
    path('sub-admin-logout', views.sub_admin_logout, name='sub_admin_logout'),
    path('start-service/<str:name>/<str:svr>', views.start_service, name='start_service'),
    path('close-service/<str:name>/<str:svr>', views.close_service, name='close_service'),
    # -------------------------User-------------------------------------------------------------
    path('user-home-page', views.user_home_page, name='user_home_page'),
    path('comms-tools', views.comm_tools, name='comm_tools'),
    path('updater', views.updater, name='updater'),
    path('sql-jobs', views.sql_jobs, name='sql_jobs'),
    path('user-logout', views.user_logout, name='user_logout'),
    
]