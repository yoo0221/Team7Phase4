from django.shortcuts import render, redirect
from main import models
import os 
from django.utils import timezone
from django.contrib.auth.decorators import login_required


os.chdir('C:\\oracle\\instantclient_21_7') 
os.putenv('NLS_LANG', 'AMERICAN_AMERICA.UTF8')

import cx_Oracle as ora
connect  = ora.connect('project','project','localhost:1521/orcl')
# connect  = ora.connect('team7','comp322','localhost:1521/orcl')
cursor = connect.cursor()

# Create your views here.
@login_required
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

@login_required
def courseSearch(request):
    list = []
    list2 = []
    key = 'NULL'
    return render(request, 'courseSearch.html', {'key':key, 'list':list,'list2':list2})

@login_required
def courseDetail(request, courseid):
    query = ("select C.name, P.name,P.location_city,P.location_district,P.location_street, P.location_address, P.placeid, C.courseid" + 
            " from (course C join course_consist CC on C.courseID=CC.courseID)" +
             " join place P on P.placeID=CC.placeID where C.courseID ="+ str(courseid))
    cursor.execute(query) 
    list1 = []
    for rows in cursor:
        list1.append(rows)  
    coursename = rows[0]
    query = "select text, author, created_time from course_comment where courseid = " + str(courseid)
    cursor.execute(query) 
    list2 = []
    for rows in cursor:
        list2.append(rows)
    return render(request, 'courseDetail.html',{ 'coursename':coursename,'list1':list1,'list2':list2,'courseid':courseid})

@login_required
def placeDetail(request, placeid):
    query = "select name, location_city,location_district,location_street,location_address from place where placeid = " + str(placeid)
    query2 = "select categoryname from place_in_category where placeid = " + str(placeid)

    cursor.execute(query)
    list1 = []
    list2 = []
    for rows in cursor:
        list1.append(rows)
    cursor.execute(query2)
    for rows in cursor:
        list2.append(rows)
    query3 = "select text, author, created_time from place_comment where placeid = " + str(placeid)
    cursor.execute(query3)
    list3 = []
    for rows in cursor:
        list3.append(rows)
    return render(request, 'placeDetail.html',{'list1':list1,'list2':list2,'list3':list3,'placeid':placeid})

@login_required
def placeRegist(request):
    query = "select * from category"
    cursor.execute(query)
    list = []
    for rows in cursor:
        list.append(rows)
    return render(request, 'placeRegist.html',{'list':list})

@login_required
def registComplete(request):
    return render(request, 'registComplete.html')

@login_required
def courseRegist(request):
    query = "select placeid, name, location_city, location_district, location_street, location_address from place"
    cursor.execute(query)
    list = []
    for rows in cursor:
        list.append(rows)
    return render(request, 'courseRegist.html',{'list':list})

@login_required
def placeRegSubmit(request):
    connect.begin()
    placeName = request.POST['placeName']
    placeCity = request.POST['placeCity']
    placeDistrict = request.POST['placeDistrict']
    placeStreet = request.POST['placeStreet']
    placeAddress = request.POST['placeAddress']
    categoryList = request.POST.getlist('categories[]')
    query = "select max(placeid) from place"
    cursor.execute(query)
    for rows in cursor:
        max_placeid = int(rows[0])
    maker_id = 1
    query = ("insert into place values("+str(max_placeid+1)+ ",'"+ placeCity +"','"+placeDistrict+"','"+placeStreet +
            "','"+placeAddress+"',"+str(maker_id)+",NULL, '" +placeName+"')")
    
    cursor.execute(query)
    # print(query)
    for category in categoryList:
        query2 = "insert into place_in_category values('"+category+"',"+str(max_placeid+1)+")"
        cursor.execute(query2)
    connect.commit()
    return redirect('registComplete')

@login_required
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

@login_required
def courseCommentRegist(request,courseid):
    comment = request.POST['comment_txt']
    query = "select max(commentid) from course_comment"
    cursor.execute(query)
    for rows in cursor:
        max_commentid = int(rows[0])
    maker_id = 'user1'
    time = timezone.localtime()
    #'2021-01-01 19:18:45
    created_time = time.strftime('%Y-%m-%d')+" "+time.strftime('%X')
    #created_time = str(time[0])+'-'+str(time[1])+'-'+str(time[2])+' '+str(time[3])+':'+str(time[4])+':'+str(time[5])
    query = ("insert into course_comment values ("+ str(max_commentid+1)+",'"
            + comment+"','"+maker_id+"',"+ "to_date('"+created_time+"', "+"'yyyy-mm-dd hh24:mi:ss'),"+str(courseid)+")")
    # print(query)
    cursor.execute(query)
    connect.commit()
    query = ("select C.name, P.name,P.location_city,P.location_district,P.location_street, P.location_address, P.placeid, C.courseid" + 
            " from (course C join course_consist CC on C.courseID=CC.courseID)" +
             " join place P on P.placeID=CC.placeID where C.courseID ="+ str(courseid))
    cursor.execute(query) 
    list1 = []
    for rows in cursor:
        list1.append(rows)  
    coursename = rows[0]
    query = "select text, author, created_time from course_comment where courseid = " + str(courseid)
    cursor.execute(query) 
    list2 = []
    for rows in cursor:
        list2.append(rows)
    return render(request, 'courseDetail.html',{ 'coursename':coursename,'list1':list1,'list2':list2,'courseid':courseid})


@login_required
def placeCommentRegist(request, placeid):
    comment = request.POST['comment_txt']
    query = "select max(commentid) from place_comment"
    cursor.execute(query)
    for rows in cursor:
        max_commentid = int(rows[0])
    maker_id = 'user1'
    time = timezone.localtime()
    #'2021-01-01 19:18:45
    created_time = time.strftime('%Y-%m-%d')+" "+time.strftime('%X')
    query = ("insert into place_comment values ("+ str(max_commentid+1)+",'"
            + comment+"','"+maker_id+"',"+ "to_date('"+created_time+"', "+"'yyyy-mm-dd hh24:mi:ss'),"+str(placeid)+")")
    cursor.execute(query)
    connect.commit()

    query = "select name, location_city,location_district,location_street,location_address from place where placeid = " + str(placeid)
    query2 = "select categoryname from place_in_category where placeid = " + str(placeid)

    cursor.execute(query)

    list1 = []
    list2 = []
    for rows in cursor:
        list1.append(rows)
    cursor.execute(query2)
    for rows in cursor:
        list2.append(rows)
    query3 = "select text, author, created_time from place_comment where placeid = " + str(placeid)
    cursor.execute(query3)
    list3 = []
    for rows in cursor:
        list3.append(rows)
    return render(request, 'placeDetail.html',{'list1':list1,'list2':list2,'list3':list3,'placeid':placeid})

@login_required
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

@login_required
def test(request):
    return render(request, 'bootstraptest.html')
