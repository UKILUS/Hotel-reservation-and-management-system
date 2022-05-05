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
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        is_admin = request.form['is_admin']
        print(username)
        print(password)
        user = login_select_username(username, is_admin)
        print(user)
        print([0][0])
        if len(user) >0 and user[0][0] == md5vale(password):
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
                return render_template('login.html', msg="账号密码错误,请重新输入")


@user.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        mobile = request.form['mobile']
        is_admin = request.form['is_admin']
        code = request.form['code']
        print(username)
        print(email)
        print(password)
        print(mobile)

        if len(password) < 3:
            return render_template('register.html', msg="密码长度错误！")

        if is_phone(mobile) ==  False:
            return render_template('register.html', msg="手机号格式不正确")
        if is_email(email) ==  False:
            return render_template('register.html', msg="邮箱格式不正确")

        if is_admin == "1" and code !="888888":
            return render_template('register.html', msg="管理员特殊码错误")
        if is_admin == "2" and code !="999999":
            return render_template('register.html', msg="BOSS特殊码错误")



        user = login_select_username_reg(username)
        print("============")
        print(user)
        print([0][0])
        print(len(user))
        if len(user) >0:
            return render_template('register.html', msg="用户名重复,请重新输入")
        else:
            print("******")
            user = login_select_email(email)
            print(len(user))
            if len(user) > 0 :
                return render_template('register.html', msg="email重复,请重新输入")
            else:
                data = [
                    (username, email, mobile, md5vale(password), is_admin),
                ]
                if insert_user(data):
                    return redirect('/login')
                else:
                    return render_template('register.html', msg="新建失败,请重新输入")


@user.route("/", methods=['GET', 'POST'], endpoint='index')
def index():
    user = session.get('user')
    all_categories = get_all_category()
    print(all_categories)
    return render_template('index.html', user=user, all_categories=all_categories)

@user.route("/user_info", methods=['GET', 'POST'], endpoint='user_info')
def user_info():
    user = session.get('user')
    user_info = get_user_by_username(user)
    user_info["juese"] = get_juese(user_info["is_admin"])
    return render_template('user_info.html', user_info=user_info, user=user)


@user.route("/company", methods=['GET', 'POST'], endpoint='company')
def company():
    user = session.get('user')
    return render_template('company.html', user=user)


@user.route("/category", methods=['GET'], endpoint='category')
@wapper
def category():
    cid = request.args.get("id")
    searchkey = request.args.get("searchkey", "")
    mtype = request.args.get("mtype", "")
    user = session.get('user')
    category = get_category_by_id(cid)

    rooms = []
    if searchkey == "":
        rooms = get_room_by_categoryid(cid)
    else:
        if mtype == "chao":
            rooms = get_category_room_by_chao_search(searchkey, cid)
        elif mtype == "chuang":
            if searchkey == "Have a window":
                rooms = get_category_room_by_chuang("1", cid)
            else:
                rooms = get_category_room_by_chuang("0", cid)
    print(category)

    for i in range(len(rooms)):
        order = get_can_order_status_by_room(rooms[i]["id"])
        if len(order) > 0:
            rooms[i]["status"] = "1"
        else:
            rooms[i]["status"] = "0"
        print(rooms[i]["status"])
    print(rooms)
    return render_template('category.html', user=user, category=category, rooms=rooms, cid=cid)



def get_status_by_room(room):
    current = get_now_stamp()
    status1 = get_status1_by_room(room["id"], current)
    print(status1)
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

@user.route("/room_book", methods=['GET'], endpoint='room_book')
@wapper
def room_book():
    cid = request.args.get("id")
    user = session.get('user')
    userinfo = get_user_by_username(user)
    room = get_room_by_id(cid)
    print(room)
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
            return render_template('errinfo.html', user=user,msg="您选择了叫醒服务器却没有选择时间，返回重新填写！" )
    data = [
            (user_id, room_id, category_id, str(category["price"].split(".")[0]), weak, need_weak, str(get_stamp_by_time(begin + " 12:00:00")),str(get_stamp_by_time(end + " 12:00:00")),username,mobile,category["name"],room["descp"],),
        ]
    insert_order(data)
    orderid = max_order_id();

    print(category["price"])
    ding = str(float(category["price"]) * 0.2)
    money_data = [
        (orderid, ding, "1", "1",),
    ]
    insert_order_money(money_data)
    print(orderid)
    return render_template('money_confirm.html', user=user, category=category, userinfo=userinfo, begin=begin, end=end, need_weak=need_weak, weak=weak, orderid=orderid, ding=ding)


@user.route("/order", methods=['GET'], endpoint='order')
@wapper
def order():
    cid = request.args.get("id")
    status = request.args.get("status", "")
    user = session.get('user')
    userinfo = get_user_by_username(user)
    order = get_order_by_id(cid)
    if status != "":
        update_order_status_by_id(cid, "1")
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
    user = session.get('user')
    userinfo = get_user_by_username(user)
    orders = get_all_order_by_user(userinfo["id"])
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
    rid = request.args.get("rid")
    user = session.get('user')
    userinfo = get_user_by_username(user)
    order = get_order_by_id(rid)
    order["begin"] = get_time_by_stamp(order["begin_time"])
    order["end"] = get_time_by_stamp(order["end_time"])
    return render_template('delay_time.html', user=user, order=order, userinfo=userinfo)

@user.route("/delete_order", methods=['GET', 'POST'], endpoint='delete_order')
@wapper
def delete_order():
    if request.method == "GET":
        rid = request.args.get("rid")
        user = session.get('user')
        userinfo = get_user_by_username(user)
        order = get_order_by_id(rid)
        order["begin"] = get_time_by_stamp(order["begin_time"])
        order["end"] = get_time_by_stamp(order["end_time"])
        order["status"] = get_int_status_by_time(order["begin_time"], order["end_time"], get_now_stamp(),order["status"])
        ding = str(float(order["price"]) * 0.2)
        return render_template('delete_order.html', user=user, order=order, userinfo=userinfo, ding=ding)
    if request.method == "POST":
        oid = request.form.get("oid")
        order = get_order_by_id(oid)
        order["begin"] = get_time_by_stamp(order["begin_time"])
        order["end"] = get_time_by_stamp(order["end_time"])
        order["status"] = get_int_status_by_time(order["begin_time"], order["end_time"], get_now_stamp(),
                                                 order["status"])
        if(order["status"]) != "4":
            update_order_money_delete_by_id(oid)
        update_order_delete_by_id(oid, get_now_stamp())
        return redirect("/order?id=" + oid)


@user.route("/delay_order", methods=['POST'], endpoint='delay_order')
@wapper
def delay_order():
    print(request.form)
    oid = request.form.get("oid")
    delay = request.form.get("delay")
    delay_stamp = str(get_stamp_by_time(delay + " 12:00:00"))
    update_end_time_by_id(oid, delay_stamp)
    return redirect("/order?id=" + oid)


@user.route("/pay_order", methods=['GET', 'POST'], endpoint='pay_order')
@wapper
def pay_order():
    if request.method == "GET":
        rid = request.args.get("rid")
        user = session.get('user')
        userinfo = get_user_by_username(user)
        order = get_order_by_id(rid)
        order["begin"] = get_time_by_stamp(order["begin_time"])
        order["end"] = get_time_by_stamp(order["end_time"])
        ding = str(float(order["price"]) * 0.2)
        extra = get_order_ex_sum_by_id(rid)
        order_money = get_order_money_sum_by_id(rid)
        print(float(order["price"]))
        print(float(ding))
        print(float(extra))
        last_money = float(order["price"]) - float(ding) + float(extra)
        print(last_money)
        return render_template('pay_order.html', user=user, order=order, userinfo=userinfo, ding=ding, extra=extra, order_money=order_money, last_money=last_money)

@user.route("/pay_confirm", methods=['GET'], endpoint='pay_confirm')
@wapper
def pay_confirm():
    print(request.get_data())
    oid = request.args.get("rid")
    print("============")
    print(oid)
    order = get_order_by_id(oid)
    update_order_status_2_by_id(order["id"])

    print(order["price"])
    ding = str(float(order["price"]) * 0.8)
    money_data = [
        (order["id"], ding, "2", "1",),
    ]
    insert_order_money(money_data)
    return redirect("/order?id=" + oid)


@user.route("/all_rooms", methods=['GET', 'POST'], endpoint='all_rooms')
def all_rooms():
    searchkey = request.args.get("searchkey", "")
    mtype = request.args.get("mtype", "")
    user = session.get('user')
    all_categories = get_all_category()
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
        if mtype == "chao":
            rooms = get_room_by_chao_search(searchkey)
        elif mtype == "chuang":
            if searchkey == "Have a window":
                rooms = get_room_by_chuang("1")
            else:
                rooms = get_room_by_chuang("0")
        else:
            cate = get_category_by_price(searchkey)
            if cate != {}:
                rooms = get_room_by_categoryid(cate["id"])
            else:
                rooms = []
        for room in rooms:
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
    session['user'] = request.form.get('')
    return redirect('/login')


@user.route('/modify_user', methods=['GET', 'POST'])
def modify_user():
    user = session.get('user')
    user_info = get_user_by_username(user)
    user_info["juese"] = get_juese(user_info["is_admin"])
    if request.method == 'POST':
        uid = request.form['uid']
        email = request.form['email']
        mobile = request.form['mobile']

        if is_phone(mobile) == False:
            return render_template('user_info.html', msg="手机号格式错误！", user_info=user_info, user=user)
        if is_email(email) == False:
            return render_template('user_info.html', msg="email格式错误！", user_info=user_info, user=user)
        user_id = get_user_by_id(uid)
        if user_id == {}:
            return render_template('user_info.html', msg="用户不存在", user_info=user_info, user=user)

        if email == "" or len(email) < 6 :
            return render_template('user_info.html', msg="邮箱必须大于6位", user_info=user_info, user=user)

        if user_id["email"] != email:
            user = get_user_by_email(email)
            if user != {}:
                return render_template('user_info.html', msg="email已存在！", user_info=user_info, user=user)
        update_user__by_id(uid, mobile, email)

        return redirect('/user_info')

