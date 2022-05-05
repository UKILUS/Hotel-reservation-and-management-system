#-*- coding:utf-8 -*-
# author: 梁欣雨
# datetime:2021/1/4 18:02

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

    return render_template('user_info.html', user_info=user_info, user=user)


@user.route("/company", methods=['GET', 'POST'], endpoint='company')
def company():
    user = session.get('user')
    return render_template('company.html', user=user)



@user.route('/logout', methods=['GET'], endpoint='logout')
@wapper
def logout():
    session['user'] = request.form.get('')
    return redirect('/login')

