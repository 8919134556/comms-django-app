from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib import messages
from django.template import loader
from django.db import connection
from .models import *
from django.utils.crypto import get_random_string
from django.core.mail import EmailMessage
import psutil
import subprocess
import pygetwindow as gw
import os
import time
import pyautogui
import cv2
import numpy as np
import socket, struct, pickle
import codecs
from datetime import datetime
import pyodbc 







#----------------------------------------------------Login---------------------------------------------------------


def login_page(request):
    sv = Server_details.objects.all()
    d = datetime.now()
    if request.method == "POST":
        email = request.POST.get('email')
        pwd = request.POST.get ('pws')
        user = request.POST.get ('user')
        server = request.POST.get ('server')
        try:
            if user == "Admin":
                login_user = Comms_user.objects.get(emp_email=email, emp_pwd = pwd, emp_role="Admin")
                request.session["admin_name"] = login_user.emp_name
                messages.success(request, "welcome")
                return redirect('admin_dashboard') 
            elif user == "Sub-Admin":
                login_user = Comms_user.objects.get(emp_email=email, emp_pwd = pwd, emp_role ="Sub-Admin")
                request.session["sub_admin_name"] = login_user.emp_name
                if  Comms_user.objects.filter(server_name = server).exists():
                    d = Comms_user.objects.get(server_name = server)
                    messages.error (request, d.emp_name +" "+ "Uses The Server")
                else:
                    data = get_object_or_404(Comms_user, emp_email= email)
                    data.server_name = server
                    data.save(update_fields=["server_name"])
                    data.save()
                    employees = log_activity.objects.create(emp_name=request.session["sub_admin_name"],service_name='Null', Action="Null", login_time = d)
                    employees.save()
                    
                    messages.success(request, "welcome")
                    return redirect('sub_admin', server) 
            elif user == "user":
                login_user = Comms_user.objects.get(emp_email=email, emp_pwd = pwd, emp_role = "user")
                request.session["User_name"] = login_user.emp_name
                messages.success(request, "welcome")
                return redirect('user_home_page') 
            else:
                messages.success(request, "bad credential Please Register")
        except:
            messages.error(request, "bad credential Please Register")
            return redirect('login_page')
    return render (request, './comms/login.html', {'view' : sv})

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            data = get_object_or_404(Comms_user, emp_email= email)
            chars =  'abcdefghijklmnopqrstuvwxyz0123456789'
            order_id = get_random_string(8, chars)
            data.emp_pwd = order_id
            data.save(update_fields=["emp_pwd"])
            data.save()
            email = EmailMessage('New Password',f'\nHere Your New Credential\nUser Name : {email}\nPassword : {order_id}\n\n\nThank you.....!', to=[email])
            email.send()
            messages.success(request, "Thank you Yor Password Sent to you mail")
            return redirect("login_page")
        except:
            messages.error(request, "unable to Find your Details Pls Register")
    return render (request, "./comms/forgot_password.html")



#---------------------------------------------------------Admin---------------------------------------------------------------------------




def admin_dashboard(request):
    view = request.session["admin_name"]
    u = Comms_user.objects.all()
    user = len(u)
    admin = len(u.filter(emp_role='admin'))
    sub_admin = len(u.filter(emp_role='Sub-Admin'))
    total_user = len(u.filter(emp_role='user'))
    total_server = Server_details.objects.all()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM COMMSTool where Service_name = 'Comms'")
    result_set = cursor.fetchall()
    total_comms = len(result_set)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM COMMSTool where Service_name = 'Updator'")
    result = cursor.fetchall()
    total_updaters = len(result)
    context={
        'view' : view,
        'user' : user, 
        "admin" : admin,
        "Sub_Admin": sub_admin, 
        "Total_user" : total_user,
        "tss" : total_server,
        "comms" : total_comms,
        "updaters": total_updaters,
    }
    return render (request, "./comms/dashboard.html", context=context)


def view_service(request):
    svr = Server_details.objects.all()
    current_user = request.session["admin_name"]
    today = datetime.today().strftime('%Y-%m-%d')
    try:
        if request.method == 'POST':
            select = request.POST['server']
            cursor = connection.cursor()
            cursor.execute('SELECT Client_Name, TRACKTIME_LATEST FROM COMMSTool')
            result_set = cursor.fetchall()
            ip = Server_details.objects.get(server_name = select)
            HEADERSIZE = 10
            client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            HOST = ip.server_ip
            PORT = ip.port_num
            client_socket.connect((HOST, PORT))
            d = ("null")
            a = pickle.dumps(d)
            msg = bytes(a)
            client_socket.sendall(msg)
            full_msg = b''
            new_msg = True
            while True:
                msg = client_socket.recv(16)
                if new_msg:
                    msglen = int(msg[:HEADERSIZE])
                    new_msg = False
                full_msg += msg
                if len(full_msg)-HEADERSIZE == msglen:
                    da, ti = pickle.loads(full_msg[HEADERSIZE:])
                    new_msg = True
                    full_msg = b""
                    break
            request.session["window_list"] = da
            context ={
                "view" : result_set,
                "view1": request.session["window_list"],
                "user_name" : current_user,
                'svr' : svr,
                'today_date' : today,
                'current_date': ti,
            }
        else:
            context = {
            'svr' : svr,
            "user_name" : current_user,
        }
    except:
        messages.error(request, "Server connection Failed ")
        context = {
            'svr' : svr,
            "user_name" : current_user,
        }
    return render (request, './comms/view-services.html',  context=context)


def add_user(request):
    current_user = request.session["admin_name"]
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        select = request.POST['gender']
        role = request.POST['role']
        chars =  'abcdefghijklmnopqrstuvwxyz0123456789'
        order_id = get_random_string(8, chars)
        if  Comms_user.objects.filter(emp_email=email).exists():
            messages.error (request, "Email alredy exist")
        else:
            employees = Comms_user.objects.create(emp_name=name,emp_email=email,emp_pwd=order_id,emp_gender=select,emp_role = role)
            employees.save()
            email = EmailMessage('Comms-Tool Credential !!!',f'Dear {name},\nHere Your Comms-Tool Credential:\nUser Name : {email}\nPassword : {order_id}\n   Thank you.....!', to=[email])
            email.send()
            messages.success(request, "successfully added.")
    return render (request, './comms/add-user.html', {"user_name" : current_user})


def view_user(request):
    current_user = request.session["admin_name"]
    data = Comms_user.objects.all()
    return render (request, "./comms/view-user.html", {"user_name" : current_user, 'data' : data})


def logout(request):
    del request.session["admin_name"]
    return redirect("login_page")

# ---------------------------------------------------Sub-Admin-----------------------------------------------------------
def sub_admin(request, name):
    today = datetime.today().strftime('%Y-%m-%d')
    current_user = request.session["sub_admin_name"]
    try:
        cursor = connection.cursor()
        cursor.execute('SELECT Client_Name, TRACKTIME_LATEST, Service_name FROM COMMSTool')
        result_set = cursor.fetchall()
        ip = Server_details.objects.get(server_name = name)
        HEADERSIZE = 10
        client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        HOST = ip.server_ip
        PORT = ip.port_num
        client_socket.connect((HOST, PORT))
        d = ("null")
        a = pickle.dumps(d)
        msg = bytes(a)
        client_socket.sendall(msg)
        full_msg = b''
        new_msg = True
        while True:
            msg = client_socket.recv(16)
            if new_msg:
                msglen = int(msg[:HEADERSIZE])
                new_msg = False
            full_msg += msg
            if len(full_msg)-HEADERSIZE == msglen:
                da, time = pickle.loads(full_msg[HEADERSIZE:])
                new_msg = True
                full_msg = b""
                break
        request.session["window_list"] = da
       
        context ={
            "view" : result_set,
            "view1": request.session["window_list"],
            "user_name" : current_user,
            'svr' : name,
            'current_date': time,
            'today_date' : today,
        }
    except:
        messages.error(request, "Server Connection Failed")
        context = {
        'svr' : name,
        "user_name" : current_user,
    }
    return render(request, "./comms/sub-admin.html", context=context)

def sub_admin_updater(request, name):
    today = datetime.today().strftime('%Y-%m-%d')
    current_user = request.session["sub_admin_name"]
    try:
        cursor = connection.cursor()
        cursor.execute('SELECT Client_Name, TRACKTIME_LATEST, Service_name FROM COMMSTool')
        result_set = cursor.fetchall()
        ip = Server_details.objects.get(server_name = name)
        HEADERSIZE = 10
        client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        HOST = ip.server_ip
        PORT = ip.port_num
        client_socket.connect((HOST, PORT))
        d = ("null")
        a = pickle.dumps(d)
        msg = bytes(a)
        client_socket.sendall(msg)
        full_msg = b''
        new_msg = True
        while True:
            msg = client_socket.recv(16)
            if new_msg:
                msglen = int(msg[:HEADERSIZE])
                new_msg = False
            full_msg += msg
            if len(full_msg)-HEADERSIZE == msglen:
                da, time = pickle.loads(full_msg[HEADERSIZE:])
                new_msg = True
                full_msg = b""
                break
        request.session["window_list"] = da
       
        context ={
            "view" : result_set,
            "view1": request.session["window_list"],
            "user_name" : current_user,
            'svr' : name,
            'current_date': time,
            'today_date' : today,
        }
    except:
        messages.error(request, "Server Connection Failed")
        context = {
        'svr' : name,
        "user_name" : current_user,
    }
    return render(request, "./comms/sub-admin-updater.html", context=context)

def sub_admin_sql_job(request, name):
    today = datetime.today().strftime('%Y-%m-%d')
    current_user = request.session["sub_admin_name"]
    try:
        d = conn(name)
        if d == "Failed":
            messages.success(request, "Server DB Connection Failed")
            return redirect(user_home_page)
        else:
            d.execute("exec [dbo].[job_activity]")
            result_set = d.fetchall()
            context={
                "user_name" : current_user,
                'svr' : name,
                "view" : result_set
                }
    except:
        messages.error(request, "Server Connection Failed")
        context = {
            'svr' : name,
            "user_name" : current_user,

        }
    return render(request, "./comms/sub-admin-sql-job.html", context=context)


def start_service(request, name, svr):
    try:
        date = datetime.now()
        sub_admin_name = request.session["sub_admin_name"]
        file_name = name
        client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        ip = Server_details.objects.get(server_name = svr)
        HOST = ip.server_ip
        PORT = ip.port_num
        client_socket.connect((HOST, PORT))
        d = ("start", file_name)
        a = pickle.dumps(d)
        msg = bytes(a)
        client_socket.sendall(msg)
        employees = log_activity.objects.create(emp_name=sub_admin_name,service_name=file_name, Action="Start", action_track_time=date)
        employees.save()
        return redirect("sub_admin", svr)
    except:
        messages.error(request, "Unable to Start the service")
        return redirect ("sub_admin", svr)



def close_service(request, name, svr):
    try:
        date = datetime.now()
        sub_admin_name = request.session["sub_admin_name"]
        file_name = name
        client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        ip = Server_details.objects.get(server_name = svr)
        HOST = ip.server_ip
        PORT = ip.port_num
        client_socket.connect((HOST, PORT))
        d = ("stop", file_name)
        a = pickle.dumps(d)
        msg = bytes(a)
        client_socket.sendall(msg)
        employees = log_activity.objects.create(emp_name=sub_admin_name,service_name=file_name, Action="Stop", action_track_time=date)
        employees.save()
        return redirect ("sub_admin", svr)
    except:
        messages.error(request, "Unable to Close the service")
        return redirect ("sub_admin", svr)

def sub_admin_logout(request):
    d = datetime.now()
    data = get_object_or_404(Comms_user, emp_name= request.session["sub_admin_name"])
    data.server_name = "NULL"
    data.save(update_fields=["emp_pwd"])
    data.save()
    employees = log_activity.objects.create(emp_name=request.session["sub_admin_name"],service_name='Null', Action="Null", logout_time=d)
    employees.save()
    del request.session["sub_admin_name"]
    return redirect ('login_page')
    




#-----------------------------------------------------User------------------------------------------------



def svr_details(name):
    ip = Server_details.objects.get(server_name = name)
    HEADERSIZE = 10
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    HOST = ip.server_ip
    PORT = ip.port_num
    client_socket.connect((HOST, PORT))
    d = ("null")
    a = pickle.dumps(d)
    msg = bytes(a)
    client_socket.sendall(msg)
    full_msg = b''
    new_msg = True
    while True:
        msg = client_socket.recv(16)
        if new_msg:
            msglen = int(msg[:HEADERSIZE])
            new_msg = False
        full_msg += msg
        if len(full_msg)-HEADERSIZE == msglen:
            da, ti = pickle.loads(full_msg[HEADERSIZE:])
            new_msg = True
            full_msg = b""
            break
    return  da, ti

def comms_database_details(name,ip):
    cursor = connection.cursor()
    cursor.execute("SELECT Client_Name, TRACKTIME_LATEST FROM COMMSTool WHERE (Service_name = '{0}' AND Server_IP= '{1}')".format(name, ip))
    result_set = cursor.fetchall()
    return result_set

def conn(server_name):
    ip = Server_details.objects.get(server_name = server_name)
    driver = ip.db_driver
    server = ip.db_ip
    username = ip.db_user_name
    password = ip.db_pwd
    db = ip.db_name
    try:
        conn1 = pyodbc.connect(driver=driver, server=server, database=db,
                                uid = username, pwd=password,)
        my_cursor = conn1.cursor()
        print("SQL Server connection successful")
        return my_cursor
    except:
        print("Connection Failed")
        return "Failed"

        






def user_home_page(request):
    try:
        sv = Server_details.objects.all()
        current_user = request.session["User_name"]
        context= {'list' : sv,
                    "user_name" : current_user,}
        try:
            if request.method == 'POST':
                name = request.POST['name']
                request.session["user_server"] = name
                context = {
                    'list' : sv,
                    "user_name" : current_user,
                    "user_server" : request.session["user_server"]
                }
                return redirect ('comm_tools')
        except:
            context = {
                    'list' : sv,
                    "user_name" : current_user,
                    "user_server" : request.session["user_server"]
                }
    except:
        messages.error(request, "Please Login")
        return redirect('login_page')
    
    return render (request, './comms/user-home-page.html', context=context)



def comm_tools(request):
    try:
        sv = Server_details.objects.all()
        current_user = request.session["User_name"]
        service = "Comms"
        if request.method == 'POST':
            name = request.POST['name']
            request.session["user_server"] = name
            return redirect('comm_tools')
        else:
            try:
                today = datetime.today().strftime('%Y-%m-%d')
                ip = Server_details.objects.get(server_name = request.session["user_server"])
                ip = ip.server_ip
                d = comms_database_details(service, ip)
                try:
                    s, ti = svr_details(request.session["user_server"])
                
                    context ={
                        "view" : d,
                        "view1": s,
                        'svr' : request.session["user_server"],
                        'current_date': ti,
                        'today_date' : today,
                        'list' : sv,
                        "user_name" : current_user,
                    }
                except:
                    messages.error(request, "Server Connection Failed")
                    return redirect(user_home_page)

            except:
                messages.success(request, "Please select Server")
                return redirect(user_home_page)
    except:
        messages.error(request, "Please Login")
        return redirect('login_page')

    return render(request, './comms/comms-tools.html', context=context)



def updater(request):
    try:
        sv = Server_details.objects.all()
        current_user = request.session["User_name"]
        service = "Updator"
        if request.method == 'POST':
            name = request.POST['name']
            request.session["user_server"] = name
            return redirect('comm_tools')
        else:
            try:
                today = datetime.today().strftime('%Y-%m-%d')
                ip = Server_details.objects.get(server_name = request.session["user_server"])
                ip = ip.server_ip
                d = comms_database_details(service, ip)
                try:
                    s, ti = svr_details(request.session["user_server"])
                    context ={
                        "view" : d,
                        "view1": s,
                        'svr' : request.session["user_server"],
                        'current_date': ti,
                        'today_date' : today,
                        'list' : sv,
                        "user_name" : current_user,
                    }
                except:
                    messages.error(request, "Server Connection Failed")
                    return redirect(user_home_page)
            except:
                messages.success(request, "Please select Server")
                return redirect(user_home_page)
    except:
        messages.error(request, "Please Login")
        return redirect('login_page')
    return render(request, './comms/updater.html', context=context)


def sql_jobs(request):
    sv = Server_details.objects.all()
    current_user = request.session["User_name"]
    if request.method == 'POST':
        name = request.POST['name']
        request.session["user_server"] = name
        return redirect('comm_tools')
    else:
        try:
            d = conn(request.session["user_server"])
            if d == "Failed":
               messages.success(request, "Server DB Connection Failed")
               return redirect(user_home_page)
            else:
                d.execute("exec [dbo].[job_activity]")
                result_set = d.fetchall()
                context={
                    'view' : result_set,
                    "user_name" : current_user,
                    'list' : sv,
                    'svr' : request.session["user_server"]
                    }
        except:
            messages.success(request, "Please select Server")
            return redirect(user_home_page)
    return render(request, './comms/sql-jobs.html', context=context)






def user_logout(request):
    try:
        del request.session["user_server"]
        del request.session["User_name"]
    except:
        del request.session["User_name"]
    return redirect('login_page')
