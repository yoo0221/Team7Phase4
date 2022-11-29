from django.shortcuts import render, redirect
from main import models
import os 
os.chdir('C:\\oracle\\instantclient_21_7') 
os.putenv('NLS_LANG', 'AMERICAN_AMERICA.UTF8')

import cx_Oracle as ora
connect  = ora.connect('project','project','localhost:1521/orcl')
cursor = connect.cursor()

# Create your views here.
def index(request):
    courseQuery = ("select C.courseID, C.name from course C where C.courseID <= 5")
    cursor.execute(courseQuery)
    list = []
    for rows in cursor:
        list.append(rows)
    list2 = []
    user_id = "user1"
    query = "select d.text, d.created_time from diary d, users u where u.coupleid = d.coupleid and u.username = '"+user_id+"'"
    cursor.execute(query) 
    count = 0
    for rows in cursor:
        if count <5:
            list2.append(rows)
            count += 1
    return render(request, 'index.html', {'list':list,'list2':list2})

def courseSearch(request):
    list = []
    list2 = []
    key = 'NULL'
    return render(request, 'courseSearch.html', {'key':key, 'list':list,'list2':list2})

def courseDetail(request):
    return render(request, 'courseDetail.html')

def placeDetail(request):
    return render(request, 'placeDetail.html')

def placeRegist(request):
    return render(request, 'placeRegist.html')

def registComplete(request):
    return render(request, 'registComplete.html')

def courseRegist(request):
    query = "select placeid, name, location_city, location_district, location_street, location_address from place"
    cursor.execute(query)
    list = []
    for rows in cursor:
        list.append(rows)
    return render(request, 'courseRegist.html',{'list':list})

def placeRegSubmit(request):
    placeName = request.POST['placeName']
    placeCity = request.POST['placeCity']
    placeDistrict = request.POST['placeDistrict']
    placeStreet = request.POST['placeStreet']
    placeAddress = request.POST['placeAddress']
    query = "select max(placeid) from place"
    cursor.execute(query)
    for rows in cursor:
        max_placeid = int(rows[0])
    maker_id = 1
    query = ("insert into place values("+str(max_placeid+1)+ ",'"+ placeCity +"','"+placeDistrict+"','"+placeStreet +
            "','"+placeAddress+"',"+str(maker_id)+",NULL, '" +placeName+"')")
    print(query)
    cursor.execute(query)
    connect.commit()
    return redirect('registComplete')

def courseRegSubmit(request):
    courseName = request.POST['courseName']
    placeList = request.POST.getlist('places[]')
    query = "select max(courseid) from course"
    cursor.execute(query)
    for rows in cursor:
        max_courseid = int(rows[0])
    maker_id = 1
    query = "insert into course values("+str(max_courseid+1)+",'"+courseName+"', "+str(maker_id) +")"
    print(query)
    cursor.execute(query)
    for placeid in placeList:
        query = "insert into course_consist values("+ str(max_courseid+1) +"," +str(placeid) +")"
        print(query)
        cursor.execute(query)
    connect.commit()
    return redirect('registComplete')


def courseSearchbyKey(request):
    key = request.POST['searchKey']
    list = []
    query = ("select C.courseID, C.name from course C, course_consist CC "+
            "where C.courseID=CC.courseID and CC.placeID in (select PC.placeID from place_in_category PC "+
            "where PC.categoryName like '%"+key+"%')")
    print(query)
    cursor.execute(query)    
    for rows in cursor:
        list.append(rows)
    list2 = []
    query = ("select courseid, name from course where name like '%"+key+"%'")
    cursor.execute(query)    
    for rows in cursor:
        list2.append(rows) 
    return render(request,'courseSearch.html',{'key':key, 'list':list,'list2':list2})