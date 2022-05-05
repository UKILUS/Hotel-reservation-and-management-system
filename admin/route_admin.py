#-*- coding:utf-8 -*-
# author: liang xinyu
# datetime:2022/1/4 18:02


from flask import Blueprint, request, render_template, session, redirect
from .db_admin import *
from utils import *
from json_response import *
import os
import os,sys,random,string
import datetime
import calendar


admin = Blueprint("admin", __name__)

#Define a data dictionary of extras that includes all the prices and names of hotel room extras
order_ex = {
    "yangshua":{"price":"8", "zh":"TOOTHBRUSH"},
    "kuangquanshui":{"price":"2", "zh":"MINERAL WATER"},
    "mianbao":{"price":"10", "zh":"BREAD"},
    "riyongpin":{"price":"28", "zh":"DAILY NECESSITIES"},
}
#Define a method to determine if there are values in a session and to determine permissions during registration
def admin_wapper(func):
    def inner(*args,**kwargs):
        #If there is no value in the session, enter the login screen
        if not session.get('user'):
            return redirect('/login')
        #Define a variable, user, to store the user in the session
        user = session.get('user')
        print(user)
        #If there is no session, return to the login page
        if user == None:
            return redirect('/login')
        #Define the variable get_admin_by_username () to get is_admin in the database
        is_admin = get_admin_by_username(user)
        print(user + "--online--" + str(is_admin))
        #If it is an administrator, return to the administrator page
        if is_admin:
            is_admin = is_admin[0][0]
            if is_admin == "1" or is_admin == "2":
                return func(*args,**kwargs)
            #Otherwise the prompt has no permissions
            else:
                return render_template('errinfo.html', msg="Sorry, you are not an administrator without permission！")
        else:
            return redirect('/login')

    return inner
#
@admin.route("/base_admin", methods=['GET'], endpoint='base_admin')
@admin_wapper
def base_admin():
    #Set variable user,Gets the user in the session
    user = session.get('user')
    print(user)
    #Define the variable is_admin, and call the get_admin_by_username method to pass in the user value
    is_admin = get_admin_by_username(user)
    print(is_admin)
    print(len(is_admin))
    #Determines if is_admin has a character length greater than 0
    if len(is_admin) > 0:
        is_admin = is_admin[0][0]
        print(is_admin)
        #If the value is 1, the Admin page is returned
        if is_admin == "1":
            return redirect("/admin_index")
        #If the value is 2, the BOSS page is returned
        elif is_admin == "2":
            return redirect("boss_index")
        #Otherwise, it returns the disabled permission
        else:
            return render_template('errinfo.html', msg="Sorry, you are not an administrator without permission！")
    #Return to the login page
    else:
        return redirect("/login")

@admin.route("/boss_index", methods=['GET'], endpoint='boss_index')
@admin_wapper
def boss_index():
    #Define the search fetch to be a parameter of search
    search = request.args.get('search', '')
    print(search)
    # Set variable user,Gets the user in the session
    user = session.get('user')
    #Determines if search is empty
    if search is None or search == "":
        #Define the kefang variable, call the get_all_kefang () method, and convert it to float
        kefang = get_float(get_all_kefang()[0][0])
        #Define the ding variable, call the get_all_ding () method, and convert it to float
        ding = get_float(get_all_ding()[0][0])
        # Define the ex variable, call the get_all_ex () method, and convert it to float
        ex = get_float(get_all_ex()[0][0])

    #If there is search, the value passed in search is called
    else:
        kefang = get_float(get_all_kefang_by_date(search)[0][0])
        ding = get_float(get_all_ding_by_date(search)[0][0])
        ex = get_float(get_all_ex_by_date(search)[0][0])

    #Define the total variable and calculate the total amount
    total = kefang + ding + ex

    print(total)
    print(kefang)
    print(ding)
    print(ex)

    #Define the variable room_count to store the value of the call to the get_all_room_order_count () method
    room_count = get_all_room_order_count()
    #Assign the value of room_count to I
    for i in range(len(room_count)):
        room_count[i]["room"] = get_room_by_id(room_count[i]["room_id"])
    begin = ""
    end = ""

    #Determines whether room_count is a value greater than 1
    if len(room_count) > 1:
        #Define the BEGIN variable to be the largest in the data dictionary
        begin = room_count[0]
        # Define the BEGIN variable to be the smallest in the data dictionary
        end = room_count[-1]
        #Define the variables begin_room and end_room and assign a value via get_category_by_id ()
        begin_room = get_category_by_id(begin.get("room_id"))
        end_room = get_category_by_id(end.get("room_id"))

    return render_template('boss_index.html',user=user, kefang=kefang, ding=ding,ex=ex, total=total,begin_room=begin_room.get('name'),end_room=end_room.get('name'), search=search)

#Define a method to convert STR values to float
def get_float(str):
    try:
        if str:
            return float(str)
        else:
            return 0.0

    except Exception as e:
        print(e)
        return 0.0


@admin.route("/admin_index", methods=['GET'], endpoint='admin_index')
@admin_wapper
def admin_index():
    #Define a variable, user, and assign the user of the session
    user = session.get('user')
    #Define a variable, orders, and assign a value to call get_all_order ()
    orders = get_all_order()
    #Define search and assign a value to get search in the URL
    search = request.args.get("search", "")
    print(search)
    #Determines if search is not empty
    if search != "":
        #Redefine and assign to the variable orders, passing search into get_all_order_by_user ()
        orders = get_all_order_by_user(search)
    #Assign the data transfer from Orders to I
    for i in range(len(orders)):
        #Define the orders[][] data dictionary to get the values transmitted from the get_time_by_stamp () method
        orders[i]["begin"] = get_time_by_stamp(orders[i]["begin_time"])
        orders[i]["end"] = get_time_by_stamp(orders[i]["end_time"])
        #Define the variable now to get the value transferred from the method get_now_stamp ()
        now = get_now_stamp()
        orders[i]["show"] = get_status_by_time(orders[i]["begin_time"], orders[i]["end_time"], now, orders[i]["status"])
    return render_template('admin_index.html', user=user, orders=orders)

@admin.route("/current_order", methods=['GET'], endpoint='current_order')
def current_order():
    #Define a variable, user, and assign the user of the session
    user = session.get('user')
    # Define a variable, orders, and assign a value to call get_all_order ()
    orders = get_all_order()
    # Define search and assign a value to get search in the URL
    search = request.args.get("search", "")
    print(search)
    # Determines if search is not empty
    if search != "":
        # Redefine and assign to the variable orders, passing search into get_all_order_by_user ()
        orders = get_all_order_by_user(search)
    # Assign the data transfer from Orders to I
    for i in range(len(orders)):
        # Define the orders[][] data dictionary to get the values transmitted from the get_time_by_stamp () method
        orders[i]["begin"] = get_time_by_stamp(orders[i]["begin_time"])
        orders[i]["end"] = get_time_by_stamp(orders[i]["end_time"])
        # Define the variable now to get the value transferred from the method get_now_stamp ()
        now = get_now_stamp()
        orders[i]["show"] = get_status_by_time(orders[i]["begin_time"], orders[i]["end_time"],now,orders[i]["status"])
    return render_template('admin_index.html', user=user, orders=orders)


@admin.route("/modify_room", methods=['GET'], endpoint='modify_room')
def current_order():
    # Define a variable, user, and assign the user of the session
    user = session.get('user')
    # Define a rooms, orders, and assign a value to call get_all_order ()
    rooms = get_all_room()
    print(rooms)
    # Assign the data transfer from rooms to I
    for i in range(len(rooms)):
        rooms[i]["category_name"] = get_category_by_id(rooms[i]["category_id"])["name"]
        rooms[i]["price"] = get_category_by_id(rooms[i]["category_id"])["price"]
    print(rooms)
    return render_template('modify_room.html', user=user, rooms=rooms)

@admin.route("/detail_room_admin", methods=['GET', "POST"], endpoint='detail_room_admin')
def detail_room_admin():
    #Determine whether the value is obtained
    if request.method == "GET":
        # Define a variable, user, and assign the user of the session
        user = session.get('user')
        # Define id and assign a value to get id in the URL
        id = request.args.get("id", "")
        #Define the variable room and assign the value in the method get_room_by_id () to room
        room = get_room_by_id(id)
        ##Define the variable category and assign the value in the method get_category_by_id () to category
        category = get_category_by_id(room["category_id"])
        return render_template('detail_room_admin.html', user=user, room=room, category=category)
    if request.method == "POST":
        user = session.get('user')
        #Define variables category_id, room_id, category_name, price, descp, category_img, room_name, room_orientation, room_descp,And obtain their corresponding values through request.form.get method
        category_id = request.form.get("category_id", "")
        room_id = request.form.get("room_id", "")
        category_name = request.form.get("category_name", "")
        price = request.form.get("price", "")
        descp = request.form.get("descp", "")
        category_img = request.files.get("category_img", "")
        room_name = request.form.get("room_name", "")
        room_orientation = request.form.get("room_orientation", "")
        room_descp = request.form.get("room_descp", "")

        #Define the variable room, and call get_room_by_id () and assign a value to room
        room = get_room_by_id(room_id)
        #Define the variable category, and call get_category_by_id () and assign a value to category
        category = get_category_by_id(category_id)
        print(category_img.filename)

        #Define the variable img to store the name of the image
        img = ""
        if category_img == "" or category_img.filename == "":
            img = category["img"]
        else:
            #Define the variable BASEDIR to store the full address of the current script
            # basedir = os.path.abspath(os.path.abspath(os.path.dirname(__file__)))
            basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
            print(basedir)
            #Define the variable PATH, which is stored in the static folder as the path to the img folder
            path = os.path.join(os.path.join(basedir, "static"), "img")
            #Define the variable RAN_STR to store randomly generated characters
            ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 16))
            #Define the variable imgName to store the image address
            imgName = ran_str + "."+ category_img.filename.split(".")[1]
            #Define the file_path variable to store the image address and path
            file_path = os.path.join(path, imgName)
            #Save the image to the destination address
            category_img.save(file_path)
            #Define the img variable to store the certificate address of the image
            img = '/static/img/' + imgName
        #Call the method to modify the category information
        update_category_by_id(category_id, category_name, img, price, descp)
        #Call the method to modify the room information
        update_room_by_id(room_id, room_orientation, room_name, room_descp)
        return redirect("/modify_room")


@admin.route("/back_room_admin", methods=['GET'], endpoint='back_room_admin')
def back_room_admin():
    #Define a variable, user, and assign the user of the session
    user = session.get('user')
    #Define the variable current to store the data from the call method get_now_stamp ()
    current = get_now_stamp()
    print(current)
    #Define the variable orders to store the data from the call method get_all_back_order ()
    orders = get_all_back_order(current)
    # Assign the data transfer from Orders to I
    for i in range(len(orders)):
        orders[i]["begin"] = get_time_by_stamp(orders[i]["begin_time"])
        orders[i]["end"] = get_time_by_stamp(orders[i]["end_time"])
        orders[i]["status"] = get_int_status_by_time(orders[i]["begin_time"], orders[i]["end_time"], get_now_stamp(), orders[i]["status"])
        orders[i]["status_info"] = get_zh_by_status(orders[i]["status"])
        if orders[i]["status"] == "1":
            orders[i]["show"] = "1"
        else:
            orders[i]["show"] = "0"
    return render_template('back_room_admin.html', user=user, orders=orders)

@admin.route("/need_back_admin", methods=['GET', 'POST'], endpoint='need_back_admin')
def need_back_admin():
    if request.method == "GET":
        # Define a variable, user, and assign the user of the session
        user = session.get('user')
        #Define the variable orderId to store the orderId retrieved from the URL
        orderid = request.args.get("orderid")
        #Define the order variable, store and call get_order_by_id ()
        order = get_order_by_id(orderid)
        #Define a variable of dictionary type, order[], to store and call the time of stamp type
        order["begin"] = get_time_by_stamp(order["begin_time"])
        order["end"] = get_time_by_stamp(order["end_time"])
        return render_template('need_back_admin.html', user=user, order=order, order_ex=order_ex)
    else:
        # Define a variable, user, and assign the user of the session
        user = session.get('user')
        # Define the variable orderId to store the orderId retrieved from the URL
        order_id = request.form.get("order_id", "")
        # yashua = request.form.get("yashua", "")
        # kuangquanshui = request.form.get("kuangquanshui", "")
        # paomian = request.form.get("paomian", "")
        # riyongpin = request.form.get("riyongpin", "")

        # order = get_order_by_id(order_id)
        # print(order["price"])
        # ding = str(float(order["price"]) * 0.8)
        # money_data = [
        #     (order["id"], ding, "2", "1",),
        # ]
        # insert_order_money(money_data)

        #Call the method to modify the order status
        update_order_back_by_id(order_id, get_now_stamp(), "2")
        print("============")
        #Assign the items in order_ex.items() to (key,value)
        for (key,value) in order_ex.items():
            print(key,value)
            #Define the variable key_count and get the key parameter
            key_count = request.form.get(key)
            print(key_count)
            #Define the variable total, the product of the store count and the price
            total = int(key_count) * int(value["price"])
            print(total)
            #The data variable, which stores list data, is the extra price of the order.
            data = [
                (order_id, value["zh"], value["price"], key_count, total),
            ]
            #Call the method to insert data
            insert_order_ex(data)

        return redirect("/back_room_admin")



@admin.route("/morning_room_admin", methods=['GET'], endpoint='morning_room_admin')
def morning_room_admin():
    # Define a variable, user, and assign the user of the session
    user = session.get('user')
    # Define the variable current to store the data from the call method get_now_stamp () Store the present time
    current = get_now_stamp()
    #Define the variable orders, assign a value, and call get_all_morning_order () to store the time information
    orders = get_all_morning_order()
    print(orders)
    # Assign the data transfer from Orders to I
    for i in range(len(orders)):
        orders[i]["begin"] = get_time_by_stamp(orders[i]["begin_time"])
        orders[i]["end"] = get_time_by_stamp(orders[i]["end_time"])
        orders[i]["room"] = get_room_by_id(orders[i]["room_id"])
        if orders[i]["weak_time"] == "":
            continue
        print(orders[i]["weak_time"])
        #Define the variable zaojia to get and store the time of stamp type in get_stamp_by_time ()
        zaojia = get_stamp_by_time(orders[i]["weak_time"])
        print(zaojia)
        #Determine the size of the order time and the present time. If the present time is greater than the order time, it will not be displayed
        if int(current) < int(zaojia):
            orders[i]["show"] = "1"
        else:
            orders[i]["show"] = "0"
    return render_template('morning_room_admin.html', user=user, orders=orders)

@admin.route("/all_room_admin", methods=['GET'], endpoint='all_room_admin')
def all_room_admin():
    # Define a variable, user, and assign the user of the session
    user = session.get('user')
    # Define a rooms, orders, and assign a value to call get_all_order ()
    rooms = get_all_room()
    # Assign the data transfer from Orders to I
    for i in range(len(rooms)):
        rooms[i]["category"] = get_category_by_id(rooms[i]["category_id"])
        rooms[i]["status"] = get_status_by_room(rooms[i])
    print(rooms)
    return render_template('all_room_admin.html', user=user, rooms=rooms)

#Define a function to determine the state of the room
def get_status_by_room(room):
    #Define the variable current, call get_now_stamp (), store the value between the current
    current = get_now_stamp()
    #Define the variable status1, store and call get_status1_by_room, store the value that represents the current state of the room
    status1 = get_status1_by_room(room["id"], current)
    #Returns different text room states by judging the variables representing time states
    if len(status1) > 0:
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


@admin.route("/boss_all_room_admin", methods=['GET'], endpoint='boss_all_room_admin')
def boss_all_room_admin():
    # Define a variable, user, and assign the user of the session
    user = session.get('user')
    # Define a rooms, orders, and assign a value to call get_all_order ()
    rooms = get_all_room()
    # Assign the data transfer from Orders to I
    for i in range(len(rooms)):
        rooms[i]["category"] = get_category_by_id(rooms[i]["category_id"])
        # rooms[i]["status"] = get_status_by_room(rooms[i])
        order = get_can_order_status_by_room(rooms[i]["id"])
        if len(order) > 0:
            rooms[i]["status"] = "Has been scheduled"
        else:
            rooms[i]["status"] = "No reservation"
        print(rooms[i]["status"])
    print(rooms)
    return render_template('boss_all_room_admin.html', user=user, rooms=rooms)

