from django.shortcuts import render, redirect
import string
import random
import os 
from django.utils import timezone

os.chdir('C:\\oracle\\instantclient_21_7') 
os.putenv('NLS_LANG', 'AMERICAN_AMERICA.UTF8')

import cx_Oracle as ora
# connect  = ora.connect('project','project','localhost:1521/orcl')
connect  = ora.connect('team7','comp322','localhost:1521/orcl')
cursor = connect.cursor()

def register(request):
    return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        id = request.POST['username']
        password = request.POST['password']
        # 1) id check
        user_query = ("select password from users where username='"+id+"'")
        cursor.execute(user_query)
        # 2) password check
        if cursor[0][0] == password:
            pass
            #need django auth
        else:
            redirect('login')
    else:
        return render(request, 'login.html')

def random_string():
    letters_set = string.ascii_lowercase
    random_list = random.sample(letters_set, 6)
    result = ''.join(random_list)
    return result

def create_user(request):
    id = request.POST['username']
    password = request.POST['password']
    check = request.POST['password-check']
    first_name = request.POST['first-name']
    last_name = request.POST['last-name']
    sex = request.POST['sex']
    is_code = request.POST['is-invited']
    code = ''
    # 1) id redundant check
    users_query = ("select username from users")
    cursor.execute(users_query)
    for users in cursor:
        if users[0] == id:
            return redirect('register')

    # 2) password check
    if password != check:
        return redirect('register')

    # 3) couple id check and making
    if (int(is_code) == 1) :
        code = request.POST['couple-id']
    else :
        couples_query = ("select coupleID from couple")
        cursor.execute(couples_query)
        flag = 1
        while(flag):
            flag = 0
            code = random_string()
            for couples in cursor:
                if couples[0] == code :
                    flag = 1
    # insert to users table
    insert_user_query = ("insert into users values ('"+id+"', '"+password+"', '"+ first_name +"', '"+ last_name +"', '"+sex+"', '"+ code +"' )")
    cursor.execute(insert_user_query)
    connect.commit()

    return redirect('index')