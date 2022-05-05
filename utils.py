#-*- coding:utf-8 -*-
# author: qalangtao
# datetime:2021/1/5 17:46

import hashlib
import time
import datetime
import calendar
import re

def get_zh_by_status(status):
    # -1已退订 2 已支付退房 1 到期 3已入住 4 未入住两天内 5 已经预定 6其他状态
    status_dict = {
        "-1":"subscription cancellation",
        "1":"expire",
        "2":"Check-out has been paid",
        "3":"Has been in",
        "4":"Within two days of absence",
        "5":"have booked",
        "6":"Other states"
    }
    return status_dict[status]

def md5vale(key):
    input_name = hashlib.md5()
    input_name.update(key.encode("utf-8"))
    print(key,"  ---->  ",input_name.hexdigest())
    return input_name.hexdigest()


def get_user(session, redirect):
    user = session.get('user')
    if user is None or user == "" :
        return ""
    print(user + "==>session online===<")
    return user


def get_list_by_title(inner_data, title):
    last_list = []
    for datas in inner_data:
        tmp_dict = {}
        for i in range(len(datas)):
            tmp_dict[title[i]] = str(datas[i])
        last_list.append(tmp_dict)
    return last_list


def get_dict_by_title(inner_data, title):
    tmp_dict = {}
    for datas in inner_data:
        print(title)
        print(datas)
        for i in range(len(datas)):
            tmp_dict[title[i]] = str(datas[i])
    print(tmp_dict)
    return tmp_dict


def get_stamp_by_time(mytime):
    timeArray = time.strptime(mytime, "%Y-%m-%d %H:%M:%S")
    timeStamp = int(time.mktime(timeArray))
    return timeStamp


def get_time_by_stamp(mystamp):
    timeArray = time.localtime(int(mystamp))
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime


def get_now_stamp():
    return str(int(time.time()))


def get_status_by_time(begin, end, now, status):
    if status=="-1":
        return "subscription cancellation"
    if status=="2":
        return "Check-out has been paid"
    begin = int(begin)
    end = int(end)
    now = int(now)
    if now >= end :
        return "expire"
    elif now >= begin and now <= end:
        return "Has been in"
    elif now <=begin and now >= begin - (2*24*60*60):
        return "Is to stay in"
    elif now <= begin - (2*24*60*60):
        return "have booked"
    else:
        return "state of termination"

def get_int_status_by_time(begin, end, now, status):
    #-1已退订 2 已支付退房 1 到期 3已入住 4 未入住两天内 5 已经预定未入住 6其他状态
    if status=="-1" or status == "2":
        return status
    begin = int(begin)
    end = int(end)
    now = int(now)
    print("----------------")
    print(begin)
    print(get_time_by_stamp(begin))
    print(get_time_by_stamp(end))
    print(get_time_by_stamp(now))
    if now >= end :
        return "1"
    elif now >= begin and now <= end:
        return "3"
    elif now <=begin and now >= begin - (2*24*60*60):
        return "4"
    elif now <= begin - (2*24*60*60):
        return "5"
    else:
        return "6"

def get_status_by_room(begin, end, now, status):
    if status=="-1":
        return "subscription cancellation"
    if status=="2":
        return "Check-out has been paid"
    begin = int(begin)
    end = int(end)
    now = int(now)
    if now >= end :
        return "expire"
    elif now >= begin and now <= end:
        return "Has been in"
    elif now <=begin and now >= begin - (2*24*60*60):
        return "Is to stay in"
    elif now <= begin - (2*24*60*60):
        return "have booked"
    else:
        return "state of termination"

def get_juese(admin):
    if admin == "0":
        return "domestic consumer"
    elif admin == "1":
        return "adm"
    elif admin == "2":
        return "BOSS"
    else:
        return "other"

def getBetweenMonth(begin_date):
    date_list = []
    begin_date = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(time.strftime('%Y-%m-%d', time.localtime(time.time())), "%Y-%m-%d")
    print(begin_date)
    print(end_date)
    while begin_date <= end_date:
        date_str = begin_date.strftime("%Y-%m-01 %H:%M:%S")
        date_list.append(date_str)
        begin_date = add_months(begin_date,1)
    return date_list

def add_months(dt,months):
    month = dt.month - 1 + months
    print(month)
    year = int(dt.year + month / 12)
    print(year)
    month = int(month % 12) + 1
    print(month)
    day = min(dt.day, calendar.monthrange(year, month)[1])
    return dt.replace(year=year, month=month, day=day)



def is_phone(phone):
    phone_pat = re.compile('1\d{10}')
    res = re.search(phone_pat, phone)
    if not res:
        return False
    return True

def is_email(email):
    if re.match(r'[0-9a-zA-Z_]{0,19}@qq.com', email):
        return True
    else:
        return False

if __name__ == "__main__":
    print(is_email("46513@qq.com"))
    print(is_phone("15010226955"))