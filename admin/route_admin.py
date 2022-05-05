#-*- coding:utf-8 -*-
# author: qalangtao
# datetime:2021/1/4 18:02


from flask import Blueprint, request, render_template, session, redirect
from .db_admin import *
from utils import *
from json_response import *
import os
import os,sys,random,string
import datetime
import calendar


admin = Blueprint("admin", __name__)

order_ex = {
    "yangshua":{"price":"8", "zh":"牙刷"},
    "kuangquanshui":{"price":"2", "zh":"矿泉水"},
    "mianbao":{"price":"10", "zh":"面包"},
    "riyongpin":{"price":"28", "zh":"日用品"},
}
def admin_wapper(func):
    def inner(*args,**kwargs):
        if not session.get('user'):
            return redirect('/login')
        user = session.get('user')
        print(user)
        if user == None:
            return redirect('/login')
        is_admin = get_admin_by_username(user)
        print(user + "--online--" + str(is_admin))
        if is_admin:
            is_admin = is_admin[0][0]
            if is_admin == "1" or is_admin == "2":
                return func(*args,**kwargs)
            else:
                return render_template('errinfo.html', msg="对不起，您不是管理员没有权限！")
        else:
            return redirect('/login')

    return inner

@admin.route("/base_admin", methods=['GET'], endpoint='base_admin')
@admin_wapper
def base_admin():
    user = session.get('user')
    print(user)
    is_admin = get_admin_by_username(user)
    print(is_admin)
    print(len(is_admin))
    if len(is_admin) > 0:
        is_admin = is_admin[0][0]
        print(is_admin)
        if is_admin == "1":
            return redirect("/admin_index")
        elif is_admin == "2":
            return redirect("boss_index")
        else:
            return render_template('errinfo.html', msg="对不起，您不是管理员没有权限！")
    else:
        return redirect("/login")

@admin.route("/boss_index", methods=['GET'], endpoint='boss_index')
@admin_wapper
def boss_index():

    user = session.get('user')
    kefang = get_float(get_all_kefang()[0][0])
    ding = get_float(get_all_ding()[0][0])
    ex = get_float(get_all_ex()[0][0])

    print(kefang)
    print(ding)
    print(ex)
    total = kefang + ding + ex
    print(total)

    room_count = get_all_room_order_count()
    for i in range(len(room_count)):
        room_count[i]["room"] = get_room_by_id(room_count[i]["room_id"])
    begin = ""
    end = ""
    if len(room_count) > 1:
        begin = room_count[0]
        end = room_count[-1]
        print(begin)
        print(end)
    return render_template('boss_index.html',user=user, kefang=kefang, ding=ding,ex=ex, total=total,begin=begin, end=end)

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
    user = session.get('user')
    orders = get_all_order()
    search = request.args.get("search", "")
    print(search)
    if search != "":
        orders = get_all_order_by_user(search)
    for i in range(len(orders)):
        orders[i]["begin"] = get_time_by_stamp(orders[i]["begin_time"])
        orders[i]["end"] = get_time_by_stamp(orders[i]["end_time"])
    return render_template('admin_index.html', user=user, orders=orders)

@admin.route("/current_order", methods=['GET'], endpoint='current_order')
def current_order():
    user = session.get('user')
    orders = get_all_order()
    search = request.args.get("search", "")
    print(search)
    if search != "":
        orders = get_all_order_by_user(search)
    for i in range(len(orders)):
        orders[i]["begin"] = get_time_by_stamp(orders[i]["begin_time"])
        orders[i]["end"] = get_time_by_stamp(orders[i]["end_time"])
        now = get_now_stamp()
        orders[i]["show"] = get_status_by_time(orders[i]["begin_time"], orders[i]["end_time"],now,orders[i]["status"])
    return render_template('admin_index.html', user=user, orders=orders)


@admin.route("/modify_room", methods=['GET'], endpoint='modify_room')
def current_order():
    user = session.get('user')
    rooms = get_all_room()
    print(rooms)
    for i in range(len(rooms)):
        rooms[i]["category_name"] = get_category_by_id(rooms[i]["category_id"])["name"]
        rooms[i]["price"] = get_category_by_id(rooms[i]["category_id"])["price"]
    print(rooms)
    return render_template('modify_room.html', user=user, rooms=rooms)

@admin.route("/detail_room_admin", methods=['GET', "POST"], endpoint='detail_room_admin')
def detail_room_admin():
    if request.method == "GET":
        user = session.get('user')
        id = request.args.get("id", "")
        room = get_room_by_id(id)
        category = get_category_by_id(room["category_id"])
        return render_template('detail_room_admin.html', user=user, room=room, category=category)
    if request.method == "POST":
        user = session.get('user')
        category_id = request.form.get("category_id", "")
        room_id = request.form.get("room_id", "")

        category_name = request.form.get("category_name", "")
        price = request.form.get("price", "")
        descp = request.form.get("descp", "")
        category_img = request.files.get("category_img", "")

        room_name = request.form.get("room_name", "")
        room_orientation = request.form.get("room_orientation", "")
        room_descp = request.form.get("room_descp", "")

        room = get_room_by_id(room_id)
        category = get_category_by_id(category_id)

        print(category_img.filename)
        img = ""
        if category_img == "" or category_img.filename == "":
            img = category["img"]
        else:
            # basedir = os.path.abspath(os.path.abspath(os.path.dirname(__file__)))
            basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
            print(basedir)
            path = os.path.join(os.path.join(basedir, "static"), "img")

            ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 16))
            imgName = ran_str + "."+ category_img.filename.split(".")[1]
            file_path = os.path.join(path, imgName)
            category_img.save(file_path)
            img = '/static/img/' + imgName
        update_category_by_id(category_id, category_name, img, price, descp)
        update_room_by_id(room_id, room_orientation, room_name, room_descp)
        return redirect("/modify_room")


@admin.route("/back_room_admin", methods=['GET'], endpoint='back_room_admin')
def back_room_admin():
    user = session.get('user')
    current = get_now_stamp()
    print(current)
    orders = get_all_back_order(current)
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
        user = session.get('user')
        orderid = request.args.get("orderid")
        order = get_order_by_id(orderid)
        order["begin"] = get_time_by_stamp(order["begin_time"])
        order["end"] = get_time_by_stamp(order["end_time"])
        return render_template('need_back_admin.html', user=user, order=order, order_ex=order_ex)
    else:
        user = session.get('user')
        order_id = request.form.get("order_id", "")
        # yashua = request.form.get("yashua", "")
        # kuangquanshui = request.form.get("kuangquanshui", "")
        # paomian = request.form.get("paomian", "")
        # riyongpin = request.form.get("riyongpin", "")

        order = get_order_by_id(order_id)
        print(order["price"])
        ding = str(float(order["price"]) * 0.8)
        money_data = [
            (order["id"], ding, "2", "1",),
        ]
        insert_order_money(money_data)

        update_order_back_by_id(order_id, get_now_stamp(), "2")
        print("============")
        for (key,value) in order_ex.items():
            print(key,value)
            key_count = request.form.get(key)
            print(key_count)
            total = int(key_count) * int(value["price"])
            print(total)
            data = [
                (order_id, value["zh"], value["price"], key_count, total),
            ]
            insert_order_ex(data)
        return redirect("/back_room_admin")



@admin.route("/morning_room_admin", methods=['GET'], endpoint='morning_room_admin')
def morning_room_admin():
    user = session.get('user')
    current = get_now_stamp()
    orders = get_all_morning_order()
    print(orders)
    for i in range(len(orders)):
        orders[i]["begin"] = get_time_by_stamp(orders[i]["begin_time"])
        orders[i]["end"] = get_time_by_stamp(orders[i]["end_time"])
        orders[i]["room"] = get_room_by_id(orders[i]["room_id"])
        if orders[i]["weak_time"] == "":
            continue
        print(orders[i]["weak_time"])
        zaojia = get_stamp_by_time(orders[i]["weak_time"])
        print(zaojia)
        if int(current) < int(zaojia):
            orders[i]["show"] = "1"
        else:
            orders[i]["show"] = "0"
    return render_template('morning_room_admin.html', user=user, orders=orders)

@admin.route("/all_room_admin", methods=['GET'], endpoint='all_room_admin')
def all_room_admin():
    user = session.get('user')
    rooms = get_all_room()
    for i in range(len(rooms)):
        rooms[i]["category"] = get_category_by_id(rooms[i]["category_id"])
        rooms[i]["status"] = get_status_by_room(rooms[i])
    print(rooms)
    return render_template('all_room_admin.html', user=user, rooms=rooms)


def get_status_by_room(room):
    current = get_now_stamp()
    status1 = get_status1_by_room(room["id"], current)
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
        return "已入住"
    status3 = get_status3_by_room(room["id"], current)
    if len(status3) > 0:
        return "No reservation"
    return "No reservation"


@admin.route("/boss_all_room_admin", methods=['GET'], endpoint='boss_all_room_admin')
def boss_all_room_admin():
    user = session.get('user')
    rooms = get_all_room()
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

@admin.route("/day_tongji", methods=['GET'], endpoint='day_tongji')
def day_tongji():
    user = session.get('user')

    x = []
    y = []
    begin_date = (datetime.datetime.now() - datetime.timedelta(days=30)).strftime("%Y-%m-%d")
    date_list = []
    #计算开始时间和结束时间，30天
    begin_date = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(time.strftime('%Y-%m-%d', time.localtime(time.time())), "%Y-%m-%d")
    # 计算一个列表，里面是三十天内每一天的时间
    while begin_date <= end_date:
        date_str = begin_date.strftime("%Y-%m-%d %H:%M:%S")
        date_list.append(date_str)
        begin_date += datetime.timedelta(days=1)
    #遍历时间列表，获取每一天的收入总和
    for i in range(len(date_list) - 1):
        # begin = datetime.datetime.strptime(date_list[i], "%Y-%m-%d %H:%M:%S")
        # end = datetime.datetime.strptime(date_list[i + 1], "%Y-%m-%d %H:%M:%S")
        begin_stamp = get_stamp_by_time(date_list[i])
        end_stamp = get_stamp_by_time(date_list[i+1])
        #读取数据库获取每一天的顶动感总数
        orders = get_order_by_bengin_and_end(begin_stamp, end_stamp)
        total = 0.0
        #遍历订单，加和价格
        for order in orders:
            total = total + float(order["price"])
        #放在对应的列表里，前端echarts可以使用
        if date_list[i] not in x:
            x.append(date_list[i])
            y.append(total)
    yDict = {"name": "每天收入金钱", "type": "line", "data": y}
    last = {
        "xList": x,
        "yList": [yDict],
        "titleList": ["每天收入金钱"]
    }
    return success(last)

@admin.route("/count_tongji", methods=['GET'], endpoint='count_tongji')
def count_tongji():
    user = session.get('user')

    x = []
    y = []
    begin_date = (datetime.datetime.now() - datetime.timedelta(days=30)).strftime("%Y-%m-%d")
    date_list = []
    begin_date = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(time.strftime('%Y-%m-%d', time.localtime(time.time())), "%Y-%m-%d")
    while begin_date <= end_date:
        date_str = begin_date.strftime("%Y-%m-%d %H:%M:%S")
        date_list.append(date_str)
        begin_date += datetime.timedelta(days=1)
    for i in range(len(date_list) - 1):
        # begin = datetime.datetime.strptime(date_list[i], "%Y-%m-%d %H:%M:%S")
        # end = datetime.datetime.strptime(date_list[i + 1], "%Y-%m-%d %H:%M:%S")
        begin_stamp = get_stamp_by_time(date_list[i])
        end_stamp = get_stamp_by_time(date_list[i+1])

        orders = get_order_by_bengin_and_end(begin_stamp, end_stamp)
        if date_list[i] not in x:
            x.append(date_list[i])
            y.append(len(orders))
    yDict = {"name": "每天订单数量", "type": "line", "data": y}
    last = {
        "xList": x,
        "yList": [yDict],
        "titleList": ["每天订单数量"]
    }
    return success(last)

@admin.route("/room_tongji", methods=['GET'], endpoint='room_tongji')
def room_tongji():
    user = session.get('user')

    x = []
    y = []
    rooms = get_all_room()
    for room in rooms:
        all_order = get_all_order_by_roomid(room["id"])
        if room["name"] not in x:
            x.append(room["name"])
            y.append(len(all_order))
    yDict = {"name": "每个房间订单数", "type": "bar", "data": y}
    last = {
        "xList": x,
        "yList": [yDict],
        "titleList": ["每个房间订单数"]
    }
    return success(last)


@admin.route("/shouru_tongji", methods=['GET'], endpoint='shouru_tongji')
def shouru_tongji():
    user = session.get('user')
    kefang = get_float(get_all_kefang()[0][0])
    ding = get_float(get_all_ding()[0][0])
    ex = get_float(get_all_ex()[0][0])

    last = [
        {"value":kefang, "name":"客房总收入"},
        {"value":ding, "name":"定金"},
        {"value":ex, "name":"其他收入"}
    ]
    return success(last)
