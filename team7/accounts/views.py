from django.shortcuts import render, redirect
import string
import random
import os 
from django.utils import timezone
from datetime import datetime
from django.contrib import auth
from django.contrib.auth.models import User

os.chdir('C:\\oracle\\instantclient_21_7') 
os.putenv('NLS_LANG', 'AMERICAN_AMERICA.UTF8')

import cx_Oracle as ora
# connect  = ora.connect('project','project','localhost:1521/orcl')
connect  = ora.connect('team7','comp322','localhost:1521/orcl')
cursor = connect.cursor()

def register(request):
    return render(request, 'register.html')

def shop_register(request):
    return render(request, 'shopRegister.html')

def login(request):
    if request.method == 'POST':
        id = request.POST['username']
        password = request.POST['password']
        # 1) id check
        user_query = ("select password from users where username='"+id+"'")
        cursor.execute(user_query)
        # 2) password check
        for user in cursor:
            if user[0] == password:
                user = auth.authenticate(
                    request, username=id, password=password
                )
                if user is not None:
                    auth.login(request, user)
                    return redirect('index')
                else:
                    return render(request, 'login.html', {'error':'아이디 또는 비밀번호가 올바르지 않습니다.'})
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
    start_date = request.POST['start-date']
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
        couples_query = ("select couple_name from couple")
        cursor.execute(couples_query)
        flag = 1
        while(flag):
            flag = 0
            code = random_string()
            for couples in cursor:
                if couples[0] == code :
                    flag = 1
        # couple creating
        couple_id_query = ("select max(coupleID) from couple")
        cursor.execute(couple_id_query)
        couple_id = 0
        for ids in cursor:
            couple_id = ids[0] + 1
        aware = timezone.make_aware(datetime.strptime(start_date, '%Y-%m-%d'))
        s_date = aware.strftime('%Y-%m-%d')
        couple_insert_query = ("insert into couple values('"+str(couple_id)+"', '"+ code +"', to_date('"+ s_date +"', 'yyyy-mm-dd'))")
        cursor.execute(couple_insert_query)
        connect.commit()

    # insert to users table
    # get coupleID
    get_coupleid_query = ("select coupleID from couple where couple_name='"+ code +"'")
    cursor.execute(get_coupleid_query)
    couple_id = 0
    for ids in cursor:
        couple_id = ids[0]
    insert_user_query = ("insert into users values ('"+id+"', '"+password+"', '"+ first_name +"', '"+ last_name +"', '"+sex+"', '"+ str(couple_id) +"' )")
    cursor.execute(insert_user_query)
    connect.commit()

    user = User.objects.create_user(
        username=id,
        password=password
    )
    auth.login(request, user)

    return redirect('index')

def logout(request):
    auth.logout(request)
    return redirect('login')