#-*- coding:utf-8 -*-
# author: liangxinyu
# datetime:2022/1/5 17:46

import hashlib
import time
import datetime
import calendar
import re

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