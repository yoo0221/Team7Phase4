from django.shortcuts import render, redirect
from main import models
import string
import random
import os 
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.conf import settings
os.chdir('C:\\oracle\\instantclient_21_7') 
os.putenv('NLS_LANG', 'AMERICAN_AMERICA.UTF8')

import cx_Oracle as ora
connect  = ora.connect('project','project','localhost:1521/orcl')
# connect  = ora.connect('team7','comp322','localhost:1521/orcl')
cursor = connect.cursor()

# Create your views here.
@login_required
def index(request):

    # 댓글 상위 5개의 코스
    courseQuery = ("select C.courseID, C.name, count(*) from course C join course_comment CC on C.courseID=CC.courseID group by (C.courseID, C.name) order by count(*)")
    cursor.execute(courseQuery)
    list = []
    for rows in cursor:
        list.append(rows)
        if len(list)==5:
            break;

    list2 = []
    user_id = str(request.user)
    query = "select d.text, d.created_time from diary d, users u where u.coupleid = d.coupleid and u.username = '"+user_id+"'"
    cursor.execute(query) 
    count = 0
    for rows in cursor:
        if count <5:
            list2.append(rows)
            count += 1
    # get couple_name on current user
    query = "select couple_name from couple C join users U on U.coupleID=C.coupleID where U.username='"+ user_id +"'"
    couple_name = ''
    cursor.execute(query)
    for rows in cursor:
        couple_name = rows[0]

    # couple user / shop user
    query = "select username from users where username='"+ user_id +"'"
    is_user = -1
    cursor.execute(query)
    for rows in cursor:
        is_user = 1

    query = "select shopid from shop where shopid='"+ user_id +"'"
    cursor.execute(query)
    for rows in cursor:
        is_user = 0
    
    menus = []
    if is_user == 0:
        menu_query = "select "
    return render(request, 'index.html', {'list':list,'list2':list2,'couplename':couple_name, 'is_user':is_user})

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
    query = "select name, location_city,location_district,location_street,location_address, shopid from place where placeid = " + str(placeid)
    query2 = "select categoryname from place_in_category where placeid = " + str(placeid)
    query3 = "select text, author, created_time from place_comment where placeid = " + str(placeid) + " order by created_time desc"

    list1 = []
    list2 = []
    list3 = []
    menus = []
    tel = ''
    shopid = ''
    is_shop = False
    # 장소 정보
    cursor.execute(query)
    for rows in cursor:
        list1.append(rows)
        if rows[5] is not None:
            is_shop = True
            shopid = str(rows[5])

    # 속한 카테고리 정보
    cursor.execute(query2)
    for rows in cursor:
        list2.append(rows)
    
    # 댓글 목록
    cursor.execute(query3)
    for rows in cursor:
        list3.append(rows)

    # shop 여부에 따라
    if is_shop:
        shop_tel_query = "select tel from shop where shopid='"+shopid+"'"
        cursor.execute(shop_tel_query)
        for tele in cursor:
            tel = tele
        menu_query = "select name, price, filename from menu where shopid='"+shopid+"'"
        cursor.execute(menu_query)
        for menu in cursor:
            menus.append(menu)
    
    return render(request, 'placeDetail.html',{'list1':list1,'list2':list2,'list3':list3, 'placeid':placeid, 'is_shop':is_shop, 'menus':menus, 'tel':tel})

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
    placeTotalAddress = request.POST['placeTotalAddress']
    # placeCity = request.POST['placeCity']
    # placeDistrict = request.POST['placeDistrict']
    # placeStreet = request.POST['placeStreet']
    # placeAddress = request.POST['placeAddress']
    categoryList = request.POST.getlist('categories[]')
    
    address = placeTotalAddress.split()
    if len(address) > 5:
        address.pop(2)

    placeCity, placeDistrict, placeStreet, placeAddress = address

    query = "select max(placeid) from place"
    cursor.execute(query)
    for rows in cursor:
        max_placeid = int(rows[0])
    
    get_couple_query = "select coupleID from users where username='"+str(request.user)+"'"
    maker_id = ''
    cursor.execute(get_couple_query)
    for rows in cursor:
        maker_id = int(rows[0])

    query = ("insert into place values("+str(max_placeid+1)+ ",'"+ placeCity +"','"+placeDistrict+"','"+placeStreet +
            "','"+placeAddress+"', '"+str(maker_id)+"', NULL, '" +placeName+"')")
    
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
    query = ("insert into course_comment values ("+ str(max_commentid+1)+","
            + comment+","+maker_id+","+ "to_date('"+created_time+"', 'yyyy-mm-dd hh24:mi:ss'),"+courseid+")")
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
    comment = request.POST['place-comment']
    query = "select max(commentid) from place_comment"
    max_commentid = 0
    cursor.execute(query)
    for rows in cursor:
        max_commentid = int(rows[0])

    maker_id = str(request.user)
    
    time = timezone.localtime()
    #'2021-01-01 19:18:45
    created_time = time.strftime('%Y-%m-%d')+" "+time.strftime('%X')
    #created_time = str(time[0])+'-'+str(time[1])+'-'+str(time[2])+' '+str(time[3])+':'+str(time[4])+':'+str(time[5])
    query = ("insert into place_comment values ("+ str(max_commentid+1)+",'"
            + comment+"','"+maker_id+"',"+ "to_date('"+created_time+"', 'yyyy-mm-dd hh24:mi:ss'),"+str(placeid)+")")
    cursor.execute(query)
    connect.commit()

    # query = ("select C.name, P.name,P.location_city,P.location_district,P.location_street, P.location_address, P.placeid, C.courseid" + 
    #         " from (course C join course_consist CC on C.courseID=CC.courseID)" +
    #          " join place P on P.placeID=CC.placeID where C.courseID ="+ str(placeid))
    # cursor.execute(query) 
    # list1 = []

    # for rows in cursor:
    #     list1.append(rows)  
    # coursename = rows[0]

    # query = "select text, author, created_time from course_comment where courseid = " + str(courseid)
    # cursor.execute(query) 
    # list2 = []
    # for rows in cursor:
    #     list2.append(rows)
    # return render(request, 'courseDetail.html',{ 'coursename':coursename,'list1':list1,'list2':list2,'courseid':courseid})
    return redirect('placeDetail', placeid=placeid)

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
    if request.method=='POST':
        # handle image
        files = request.FILES['file']
        dir_path = os.path.join(settings.BASE_DIR, 'media')
        img_name = rand_imgname()
        file_name = dir_path+'/img/'+img_name+'.jpg'

        destination = open(file_name, 'wb+')
        for chunk in files.chunks():
            destination.write(chunk)
        destination.close()

        #insert photo db
        db_path = '/media/img/'+img_name+'.jpg'
        query = "insert into photo values(52, 50, '"+db_path+"', NULL)"
        cursor.execute(query)
        connect.commit()
        return redirect('test')
    else:
        query = "select filename from photo where placeid=50"
        cursor.execute(query)
        imgs = []
        for rows in cursor:
            imgs.append(rows)
        return render(request, 'bootstraptest.html', {'imgs':imgs})

def rand_imgname():
    letters_set = string.ascii_lowercase
    random_list = random.sample(letters_set, 10)
    result = ''.join(random_list)
    return result

def menuRegist(request):
    shopid = str(request.user)
    if request.method=='POST':
        try:
            menuname = request.POST['menu-name']
            menuprice = request.POST['menu-price']
        except:
            return redirect('menuRegist')
        try:
            menuimg = request.FILES['menu-img']
            # 이미지 처리
            dir_path = os.path.join(settings.BASE_DIR, 'media')
            img_name = rand_imgname()
            file_name = dir_path+'/img/'+img_name+'.jpg'

            destination = open(file_name, 'wb+')
            for chunk in menuimg.chunks():
                destination.write(chunk)
            destination.close()
            db_path = '/media/img/'+img_name+'.jpg'
        except:
            db_path = 'NULL'

        # insert menu on db
        if db_path != 'NULL':
            query = "insert into menu values('"+shopid+"','"+menuname+"',"+str(menuprice)+",'"+db_path+"')"
        else:
            query = "insert into menu values('"+shopid+"','"+menuname+"',"+str(menuprice)+","+db_path+")"
        cursor.execute(query)
        connect.commit()

        return redirect('menuRegist')
    else:
        menus = []
        menu_query = "select name, price, filename from menu where shopid='"+shopid+"'"
        cursor.execute(menu_query)
        for menu in cursor:
            menus.append(menu)
        return render(request, 'menuRegist.html', {'menus':menus})
    