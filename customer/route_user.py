#-*- coding:utf-8 -*-
# author: liangxinyu
# datetime:2022/1/4 18:02

from flask import Blueprint, request, render_template, session, redirect
from .db_user import *
from utils import *
import json
user = Blueprint("user", __name__)


def wapper(func):
    def inner(*args,**kwargs):
        if not session.get('user'):
            return redirect('/login')
        print(session.get('user') + "--online--")
        return func(*args,**kwargs)
    return inner


@user.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'GET':
        return render_template('login.html')
    #Determine if there is a POST request and, if so, get the relevant information
    if request.method == 'POST':
        #Define username to store the retrieved username
        username = request.form['username']
        # Define password to store the retrieved password
        password = request.form['password']
        # Define is_admin to store the retrieved is_admin
        is_admin = request.form['is_admin']
        print(username)
        print(password)
        #Define the user variable, call and get all the user information
        user = login_select_username(username, is_admin)
        print(user)
        print([0][0])
        #Determine if there is user data, and crack the password at the same time
        if len(user) >0 and user[0][0] == md5vale(password):
            #Set the user in the session to the username in the "GET" request
            session['user'] = request.form.get('username')
            if is_admin == "0":
                return redirect('/')
            elif is_admin == "1":
                return redirect("/admin_index")
            elif is_admin == "2":
                return redirect("/boss_index")
            else:
                return redirect("/")
        else:
            #Define the variable user, call and get the user information
            user = login_select_email(username)
            if len(user) > 0 and user[0][0] == md5vale(password):
                # session['user'] = request.form.get('username')
                user_email = get_user_by_email(username)
                session['user'] = user_email["username"]
                if is_admin == "0":
                    return redirect('/')
                elif is_admin == "1":
                    return redirect("/admin_index")
                elif is_admin == "2":
                    return redirect("/boss_index")
                else:
                    return redirect("/")
            else:
                return render_template('login.html', msg="The account password is wrong, please enter it again")


@user.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        #Define the variable and assign the corresponding variable to the variable defined
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        mobile = request.form['mobile']
        is_admin = request.form['is_admin']
        code = request.form['code']

        #If the password length <;3, the length of the message is not enough
        if len(password) < 3:
            return render_template('register.html', msg="Password length error！")
        #Calling the is_phone method returns an error in the format of the phone
        if is_phone(mobile) ==  False:
            return render_template('register.html', msg="The format of the phone number is not correct")
        # Calling the is_email method returns an error in the format of the email
        if is_email(email) ==  False:
            return render_template('register.html', msg="The mailbox format is incorrect")
        # Determine if the code is correct. If not, the code code error is displayed
        if is_admin == "1" and code !="888888":
            return render_template('register.html', msg="Administrator special code error")
        if is_admin == "2" and code !="999999":
            return render_template('register.html', msg="Boss special code error")
        #Define the variable user, assign the value, and call the method login_select_username_reg (), storing the username
        user = login_select_username_reg(username)
        print("============")
        print(user)
        print([0][0])
        print(len(user))
        #Determine if user is empty
        if len(user) >0:
            return render_template('register.html', msg="Duplicate user name, please reenter")
        else:
            print("******")
            # Define the variable user and call the method,storing user information
            user = login_select_email(email)
            print(len(user))
            #If user is greater than 0, it returns to the registration page with information that has not been registered
            if len(user) > 0 :
                return render_template('register.html', msg="Email is duplicate, please enter it again")

            else:
                #Define dictionary variables to store user registration information
                data = [
                    (username, email, mobile, md5vale(password), is_admin),
                ]
                #Call the method to enter the data variable into the database
                if insert_user(data):
                    return redirect('/login')
                else:
                    return render_template('register.html', msg="New failed, please enter again")


@user.route("/", methods=['GET', 'POST'], endpoint='index')
def index():
    # Define a variable, user, to store the user in the session
    user = session.get('user')
    #Define the variable all_categories to call and store data about categories
    all_categories = get_all_category()
    print(all_categories)
    return render_template('index.html', user=user, all_categories=all_categories)

@user.route("/user_info", methods=['GET', 'POST'], endpoint='user_info')
def user_info():
    # Define a variable, user, to store the user in the session
    user = session.get('user')
    #Define the variable user_info to call and store all data about user
    user_info = get_user_by_username(user)
    user_info["juese"] = get_juese(user_info["is_admin"])
    return render_template('user_info.html', user_info=user_info, user=user)


@user.route("/company", methods=['GET', 'POST'], endpoint='company')
def company():
    # Define a variable, user, to store the user in the session
    user = session.get('user')
    return render_template('company.html', user=user)


@user.route("/category", methods=['GET'], endpoint='category')
@wapper
def category():
    #Define a variable, cid, to store information about the ID retrieved from the URL
    cid = request.args.get("id")
    #Define a variable, searchkey, to store information about the searchkey retrieved from the URL
    searchkey = request.args.get("searchkey", "")
    # Define a mtype, searchkey, to store information about the mtype retrieved from the URL
    mtype = request.args.get("mtype", "")
    # Define a variable, user, to store the user in the session
    user = session.get('user')
    # Define the variable category to call and store data about categories
    category = get_category_by_id(cid)
    #Define empty dictionary rooms to store all rooms
    rooms = []
    if searchkey == "":
        rooms = get_room_by_categoryid(cid)
    else:
        #Determine if the variable mtypy is empty
        if mtype == "chao":
            #Define the variable rooms, which stores all rooms that conform to mtype
            rooms = get_category_room_by_chao_search(searchkey, cid)
        # Determine if the variable chuang is empty
        elif mtype == "chuang":
            if searchkey == "Have a window":
                #Define the variable rooms, which stores all the rooms with Windows
                rooms = get_category_room_by_chuang("1", cid)
            else:
                #Define the variable rooms, which stores all the rooms no Windows
                rooms = get_category_room_by_chuang("0", cid)
    print(category)
    # Assign the data transfer from Orders to I
    for i in range(len(rooms)):
        #Define the variable Order, and call and store the value of the Order state transferred from the method get_can_order_status_by_room ()
        order = get_can_order_status_by_room(rooms[i]["id"])
        if len(order) > 0:
            rooms[i]["status"] = "1"
        else:
            rooms[i]["status"] = "0"
        print(rooms[i]["status"])
    print(rooms)
    return render_template('category.html', user=user, category=category, rooms=rooms, cid=cid)


def get_status_by_room(room):
    #Define the variable current to store and call the method to store the current time.
    current = get_now_stamp()
    #Define the variable status1 to store and call the room state information obtained from get_status1_by_room ()
    status1 = get_status1_by_room(room["id"], current)
    print(status1)
    #Determine if there is a value
    if len(status1) > 0:
        #If the room status is -,2, no reservation is indicated
        if status1[0]["status"] == "-1":
            return "No reservation"
        elif status1[0]["status"] == "2":
            return "No reservation"
        return "Booked but not checked in"
    status2 = get_status2_by_room(room["id"], current)
    if len(status2) > 0:
        if status2[0]["status"] == "-1":
            return "No reservation"
        elif status2[0]["status"] == "2":
            return "No reservation"
        return "Has been in"
    status3 = get_status3_by_room(room["id"], current)
    if len(status3) > 0:
        return "No reservation"
    return "No reservation"

@user.route("/room_book", methods=['GET'], endpoint='room_book')
@wapper
def room_book():
    # Define a variable, cid, to store information about the ID retrieved from the URL
    cid = request.args.get("id")
    # Define a variable, user, to store the user in the session
    user = session.get('user')
    # Define the variable user_info to call and store all data about user
    userinfo = get_user_by_username(user)
    #Define the variable room, call and assign all information about room
    room = get_room_by_id(cid)
    print(room)
    #Define the variable category, call the method, and query for information about the category by ID
    category = get_category_by_id(room["category_id"])
    print(category)
    return render_template('room_book.html', user=user, room=room, category=category, userinfo=userinfo)


@user.route("/add_order", methods=['POST'], endpoint='add_order')
@wapper
def add_order():
    print(request.form)
    username = request.form.get("username")
    room_id = request.form.get("room_id")
    user_id = request.form.get("user_id")
    category_id = request.form.get("category_id")
    mobile = request.form.get("mobile")
    begin = request.form.get("begin")
    end = request.form.get("end")
    weak = request.form.get("weak")
    need_weak = request.form.get("need_weak")

    user = session.get('user')
    userinfo = get_user_by_username(user)
    room = get_room_by_id(room_id)
    category = get_category_by_id(category_id)

    if need_weak==None:
        need_weak = ""
    else:
        if need_weak == "on" and (weak == "" or weak == None):
            return render_template('errinfo.html', user=user,msg="" )
    data = [
            (user_id, room_id, category_id, str(category["price"].split(".")[0]), weak, need_weak, str(get_stamp_by_time(begin + " 12:00:00")),str(get_stamp_by_time(end + " 12:00:00")),username,mobile,category["name"],room["descp"],begin + " 12:00:00",end + " 12:00:00",),
        ]
    insert_order(data)
    orderid = max_order_id();

    print(category["price"])

    ding = str(float(category["price"]) * 0.2)
    money_data = [
        (orderid, ding, "1", "1",),
    ]
    insert_order_money(money_data)

    day = float(get_stamp_by_time(end + " 12:00:00") - get_stamp_by_time(begin + " 12:00:00"))
    print(day)
    day_count = day/(60*60*24)
    print(day_count)



    room_money = str(float(category["price"]) * day_count)
    rooms_moneys = str(float(room_money)+float(ding))
    all_shows_money=room_money+' + Deposit:￡'+ding
    money_data1 = [
        (orderid, room_money, "2", "1",),
    ]
    insert_order_money(money_data1)

    print(orderid)
    return render_template('money_confirm.html', day_count=day_count,user=user, category=category, userinfo=userinfo, begin=begin, end=end, need_weak=need_weak, weak=weak, orderid=orderid, ding=ding, room_money=room_money,all_shows_money=all_shows_money,rooms_moneys=rooms_moneys)


@user.route("/order", methods=['GET'], endpoint='order')
@wapper
def order():
    # Define a variable, cid, to store information about the ID retrieved from the URL
    cid = request.args.get("id")
    #Define the variable status to store the room status information extracted from the URL
    status = request.args.get("status", "")
    # Define a variable, user, to store the user in the session
    user = session.get('user')
    # Define the variable user_info to call and store all data about user
    userinfo = get_user_by_username(user)
    order = get_order_by_id(cid)
    if status != "":
        update_order_status_by_id(cid, "1")
    #Define the dictionary ORDER to store the time status of the order by calling the method
    order["begin"] = get_time_by_stamp(order["begin_time"])
    order["end"] = get_time_by_stamp(order["end_time"])
    order["status"] = get_int_status_by_time(order["begin_time"], order["end_time"], get_now_stamp(),order["status"] )
    order["status_info"] = get_zh_by_status(order["status"])
    category = get_category_by_id(order["category_id"])
    print(order)
    return render_template('one_order.html', user=user, order=order, category=category,userinfo=userinfo)


@user.route("/my_all_order", methods=['GET'], endpoint='my_all_order')
@wapper
def my_all_order():
    # Define a variable, user, to store the user in the session
    user = session.get('user')
    # Define the variable user_info to call and store all data about user
    userinfo = get_user_by_username(user)
    orders = get_all_order_by_user(userinfo["id"])
    # Assign the data transfer from Orders to I
    for i in range(len(orders)):
        orders[i]["begin"] = get_time_by_stamp(orders[i]["begin_time"])
        orders[i]["end"] = get_time_by_stamp(orders[i]["end_time"])
        orders[i]["status"] = get_int_status_by_time(orders[i]["begin_time"], orders[i]["end_time"], get_now_stamp(),orders[i]["status"])
        print(orders[i]["status"])
        orders[i]["status_info"] = get_zh_by_status(orders[i]["status"])
    print(orders)
    return render_template('my_all_order.html', orders=orders, user=user)


@user.route("/delay_time", methods=['GET'], endpoint='delay_time')
@wapper
def delay_time():
    #Define the variable RID to store the RID retrieved from the URL
    rid = request.args.get("rid")
    # Define a variable, user, to store the user in the session
    user = session.get('user')
    # Define the variable user_info to call and store all data about user
    userinfo = get_user_by_username(user)
    order = get_order_by_id(rid)
    # Define the dictionary ORDER to store the time status of the order by calling the method
    order["begin"] = get_time_by_stamp(order["begin_time"])
    order["end"] = get_time_by_stamp(order["end_time"])
    return render_template('delay_time.html', user=user, order=order, userinfo=userinfo)


@user.route("/delete_order", methods=['GET', 'POST'], endpoint='delete_order')
@wapper
def delete_order():
    if request.method == "GET":
        # Define the variable RID to store the RID retrieved from the URL
        rid = request.args.get("rid")
        # Define a variable, user, to store the user in the session
        user = session.get('user')
        # Define the variable user_info to call and store all data about user
        userinfo = get_user_by_username(user)
        order = get_order_by_id(rid)
        # Define the dictionary ORDER to store the time status of the order by calling the method
        order["begin"] = get_time_by_stamp(order["begin_time"])
        order["end"] = get_time_by_stamp(order["end_time"])
        order["status"] = get_int_status_by_time(order["begin_time"], order["end_time"], get_now_stamp(),order["status"])
        #Define the variable START and End to store the time value in the ORDER table
        ding = str(float(order["price"]) * 0.2)
        day = float(float(order["begin_time"]) - float(order["end_time"]))
        day_count = day / (60 * 60 * 24)
        print(day_count)
        room_money = str(float(order["price"]) * day_count)
        total = ((float(order["price"]) * 0.2) + float(order["price"]))
        return render_template('delete_order.html', total=total, user=user, order=order, userinfo=userinfo, ding=ding,
                               room_money=room_money)

    if request.method == "POST":
        oid = request.form.get("oid")
        order = get_order_by_id(oid)
        order["begin"] = get_time_by_stamp(order["begin_time"])
        order["end"] = get_time_by_stamp(order["end_time"])
        order["status"] = get_int_status_by_time(order["begin_time"], order["end_time"], get_now_stamp(),
                                                 order["status"])
        if(order["status"]) != "4":
            update_order_money_delete_by_id(oid)
        else:
            update_order_money_delete_by_id_twoday(oid)
        update_order_delete_by_id(oid, get_now_stamp())
        return redirect("/order?id=" + oid)



@user.route("/delay_order", methods=['POST'], endpoint='delay_order')
@wapper
def delay_order():
    print(request.form)
    # Define the variable OID to get the OID in the request
    oid = request.form.get("oid")
    #Define variable delay, get delay, and save variable
    delay = request.form.get("delay")
    #Delay_stamp is defined to store the event type of stamp
    delay_stamp = str(get_stamp_by_time(delay + " 12:00:00"))

    AA=get_money_by_id(oid)

    print("*****************************************")
    print(AA)
    order = get_order_by_id(oid)
    start = int(order["begin_time"])
    print(start)
    end=(int(delay_stamp))
    count=((end-start)/(24 * 60 * 60))
    print("******************")
    print(count)
    money = str(float(order["price"]) * count)
    print(money)
    update_money_by_id(oid,money)

    #Call the method to modify the time
    update_end_time_by_id(oid, delay_stamp)
    return redirect("/order?id=" + oid,)


@user.route("/pay_order", methods=['GET', 'POST'], endpoint='pay_order')
@wapper
def pay_order():
    if request.method == "GET":
        rid = request.args.get("rid")
        user = session.get('user')
        userinfo = get_user_by_username(user)
        order = get_order_by_id(rid)
        print(order["order_end"])
        first_end = get_stamp_by_time(order["order_end"])
        print(first_end)
        print(order["end_time"])
        buquan = 0.0
        if first_end != order["end_time"]:
            cha = float(order["end_time"]) - float(first_end)
            print(cha)
            day = cha/(60*60*24)
            print(day)
            buquan = day * float(order["price"])
        print(buquan)

        order["begin"] = get_time_by_stamp(order["begin_time"])
        order["end"] = get_time_by_stamp(order["end_time"])
        ding = float(order["price"]) * 0.2
        extra = get_order_ex_sum_by_id(rid)

        zhichu = float(extra) + buquan

        # tuiqain = ding - zhichu
        #
        # print(tuiqain)

        # order_money = get_order_money_sum_by_id(rid)
        # print(float(order["price"]))
        # print(float(ding))
        # print(float(extra))
        last_money = zhichu - ding
        print(last_money)
        print(last_money)
        return render_template('pay_order.html', user=user, order=order, buquan=buquan, userinfo=userinfo, ding=ding, extra=extra, zhichu=zhichu, last_money=last_money)

@user.route("/pay_confirm", methods=['GET'], endpoint='pay_confirm')
@wapper
def pay_confirm():
    print(request.get_data())
    oid = request.args.get("rid")
    mtype = request.args.get("mtype")
    print("============")
    print(oid)
    print(mtype)
    order = get_order_by_id(oid)
    update_order_status_2_by_id(order["id"])


    first_end = get_stamp_by_time(order["order_end"])
    buquan = 0.0
    if first_end != order["end_time"]:
        cha = float(order["end_time"]) - float(first_end)
        day = cha/(60*60*24)
        buquan = day * float(order["price"])
    order["begin"] = get_time_by_stamp(order["begin_time"])
    order["end"] = get_time_by_stamp(order["end_time"])
    ding = float(order["price"]) * 0.2
    extra = get_order_ex_sum_by_id(oid)

    zhichu = float(extra) + buquan
    last_money = zhichu - ding
    print(last_money)

    if last_money > 0:
        money_data = [
            (order["id"], last_money, "3", "1",),
        ]
        insert_order_money(money_data)
    else:
        print(int(ding+last_money))
        update_order_money_by_id(oid, str(int(ding+last_money)))
    return redirect("/order?id=" + oid)



@user.route("/all_rooms", methods=['GET', 'POST'], endpoint='all_rooms')
def all_rooms():

    searchkey = request.args.get("searchkey", "")
    # Define a mtype, searchkey, to store information about the mtype retrieved from the URL
    mtype = request.args.get("mtype", "")
    # Define a variable, user, to store the user in the session
    user = session.get('user')
    #Define the variable all_categories and call the method to store all the categories information
    all_categories = get_all_category()
    #Define all_rooms to store all room information
    all_rooms = []
    if searchkey == "":
        for cat in all_categories:
            rooms = get_room_by_categoryid(cat["id"])
            for room in rooms:
                room["cate_img"] = cat["img"]
                room["cate_name"] = cat["name"]
                room["cate_price"] = cat["price"]
                all_rooms.append(room)
    else:
        # Determine if the variable mtypy is empty
        if mtype == "chao":
            # Define the variable rooms, which stores all rooms that conform to mtype
            rooms = get_room_by_chao_search(searchkey)
        # Determine if the variable chuang is empty
        elif mtype == "chuang":
            if searchkey == "Have a window":
                # Define the variable rooms, which stores all the rooms with Windows
                rooms = get_room_by_chuang("1")
            else:
                # Define the variable rooms, which stores all the rooms no Windows
                rooms = get_room_by_chuang("0")
        else:
            cate = get_category_by_price(searchkey)
            if cate != {}:
                rooms = get_room_by_categoryid(cate["id"])
            else:
                rooms = []
        #Store all Rooms information in Room
        for room in rooms:
            #Define the variable cat, call the method and store the category information
            cat = get_category_by_id(room["category_id"])
            room["cate_img"] = cat["img"]
            room["cate_name"] = cat["name"]
            room["cate_price"] = cat["price"]
            all_rooms.append(room)
    print(all_rooms)
    for i in range(len(all_rooms)):
        all_rooms[i]["status"] = get_status_by_room(all_rooms[i])

    return render_template('all_rooms.html', user=user, all_rooms=all_rooms)

@user.route('/logout', methods=['GET'], endpoint='logout')
@wapper
def logout():
    #The user in the session is null
    session['user'] = request.form.get('')
    return redirect('/login')


@user.route('/modify_user', methods=['GET', 'POST'])
def modify_user():
    # Define a variable, user, to store the user in the session
    user = session.get('user')
    # Define the variable user_info to call and store all data about user
    user_info = get_user_by_username(user)
    user_info["juese"] = get_juese(user_info["is_admin"])
    if request.method == 'POST':
        uid = request.form['uid']
        email = request.form['email']
        mobile = request.form['mobile']
        #Determine if the mobile is correct
        if is_phone(mobile) == False:
            return render_template('user_info.html', msg="The format of mobile phone number is wrong！", user_info=user_info, user=user)
        # Determine if the email is correct
        if is_email(email) == False:
            return render_template('user_info.html', msg="Email format error！", user_info=user_info, user=user)
        user_id = get_user_by_id(uid)
        if user_id == {}:
            return render_template('user_info.html', msg="User does not exist", user_info=user_info, user=user)

        if email == "" or len(email) < 6 :
            return render_template('user_info.html', msg="Mailboxes must be larger than 6 digits", user_info=user_info, user=user)

        if user_id["email"] != email:
            # Define the variable user and call the method to store the user's information
            user = get_user_by_email(email)
            if user != {}:
                # Define a variable, user, to store the user in the session
                user = session.get('user')
                # Define the variable user_info to call and store all data about user
                user_info = get_user_by_username(user)
                return render_template('user_info.html', msg="Email already！", user_info=user_info, user=user)
        update_user__by_id(uid, mobile, email)

        return redirect('/user_info')

