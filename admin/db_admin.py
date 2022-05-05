import pymysql
from db_use import UseDatebase
from utils import *

dbconfig = {'host': 'localhost',
            'user': 'root',
            'passwd': '19991119',
            'db': 'tuzi-hotel', }


def get_admin_by_username(username):
    with UseDatebase(dbconfig) as cur:
        # Splicing and executing SQL statements
        email = "SELECT `is_admin` FROM user_info WHERE username =\"" + username + "\"";
        # Execute SQL statement
        cur.execute(email)
        # save search result in a variable and convert it to string
        res = cur.fetchall()
        # return the string
        return res

def get_all_order():
    with UseDatebase(dbconfig) as cur:
        # Splicing and executing SQL statements
        sql = "SELECT * FROM `order`"
        print(sql)
        # Execute SQL statement
        cur.execute(sql)
        # save search result in a variable and convert it to string
        res = cur.fetchall()
        title = ["id", "user_id", "room_id", "category_id", "price", "weak_time", "need_weak", "begin_time", "end_time", "username", "mobile", "category_name","room_descp","status"]
        # return the string
        return get_list_by_title(res, title)

def get_all_back_order(current):
    with UseDatebase(dbconfig) as cur:
        # Splicing and executing SQL statements
        sql = "SELECT * FROM `order` where status=1";
        print(sql)
        # Execute SQL statement
        cur.execute(sql)
        # save search result in a variable and convert it to string
        res = cur.fetchall()
        title = ["id", "user_id", "room_id", "category_id", "price", "weak_time", "need_weak", "begin_time", "end_time", "username", "mobile", "category_name","room_descp","status"]
        # return the string
        return get_list_by_title(res, title)

def get_can_order_status_by_room(id):
    with UseDatebase(dbconfig) as cur:
        # Splicing and executing SQL statements
        sql = "SELECT * FROM `order` WHERE status=1 and room_id=" + "\""+ id +"\"order by id asc"
        print(sql)
        # Execute SQL statement
        cur.execute(sql)
        # save search result in a variable and convert it to string
        res = cur.fetchall()
        title = ["id", "user_id", "room_id", "category_id", "price", "weak_time", "need_weak", "begin_time", "end_time", "username", "mobile", "category_name","room_descp","status"]
        # return the string
        return get_list_by_title(res, title)

def get_all_morning_order():
    with UseDatebase(dbconfig) as cur:
        # Splicing and executing SQL statements
        sql = "SELECT * FROM `order` where need_weak='on' ";
        print(sql)
        # Execute SQL statement
        cur.execute(sql)
        # save search result in a variable and convert it to string
        res = cur.fetchall()
        title = ["id", "user_id", "room_id", "category_id", "price", "weak_time", "need_weak", "begin_time", "end_time", "username", "mobile", "category_name","room_descp","status"]
        # return the string
        return get_list_by_title(res, title)

def get_all_order_by_user(username):
    with UseDatebase(dbconfig) as cur:
        # Splicing and executing SQL statements
        sql = "SELECT * FROM `order` WHERE username=\"" + username + "\""
        print(sql)
        # Execute SQL statement
        cur.execute(sql)
        # save search result in a variable and convert it to string
        res = cur.fetchall()
        title = ["id", "user_id", "room_id", "category_id", "price", "weak_time", "need_weak", "begin_time", "end_time", "username", "mobile", "category_name","room_descp","status"]
        # return the string
        return get_list_by_title(res, title)

def get_user_by_username(username):
    with UseDatebase(dbconfig) as cur:
        # Splicing and executing SQL statements
        sql = "SELECT * FROM user_info where username=\"" + username + "\""
        print(username)
        print(sql)
        # Execute SQL statement
        cur.execute(sql)
        # save search result in a variable and convert it to string
        res = cur.fetchall()
        title = ["id", "username", "email", "password", "mobile", "is_admin"]
        # return the string
        return get_dict_by_title(res, title)


def get_all_room():
    with UseDatebase(dbconfig) as cur:
        # Splicing and executing SQL statements
        sql = "SELECT * FROM `room`"
        print(sql)
        # Execute SQL statement
        cur.execute(sql)
        # save search result in a variable and convert it to string
        res = cur.fetchall()
        title = ["id", "orientation", "have_windows", "have_book", "name", "category_id", "descp"]
        # return the string
        return get_list_by_title(res, title)

def get_category_by_id(id):
    with UseDatebase(dbconfig) as cur:
        # Splicing and executing SQL statements
        sql = "SELECT * FROM category where id=" + id
        # Execute SQL statement
        cur.execute(sql)
        # save search result in a variable and convert it to string
        res = cur.fetchall()
        title = ["id", "name", "img", "price", "descp"]
        # return the string
        return get_dict_by_title(res, title)

def update_category_by_id(id, name, img, price, descp):
    with UseDatebase(dbconfig) as cur:
        # Splicing and executing SQL statements
        sql = "UPDATE `category` set name='%s',img='%s',price='%s', descp='%s' where id='%s'" % (name, img, price, descp, id)
        print(sql)
        # Execute SQL statement
        cur.execute(sql)
        # return the string
        return "ok"

def update_room_by_id(id, orientation, name, descp):
    with UseDatebase(dbconfig) as cur:
        # Splicing and executing SQL statements
        sql = "UPDATE `room` set name='%s',orientation='%s',descp='%s' where id=%s" % (name, orientation, descp, id)
        # Execute SQL statement
        cur.execute(sql)
        # return the string
        return "ok"

def get_room_by_id(id):
    with UseDatebase(dbconfig) as cur:
        # Splicing and executing SQL statements
        sql = "SELECT * FROM room where id=" + id
        # Execute SQL statement
        cur.execute(sql)
        # save search result in a variable and convert it to string
        res = cur.fetchall()
        title = ["id", "orientation", "have_windows", "have_book", "name", "category_id", "descp"]
        # return the string
        return get_dict_by_title(res, title)

def get_status1_by_room(id, current):
    with UseDatebase(dbconfig) as cur:
        # Splicing and executing SQL statements
        sql = "SELECT * FROM `order` WHERE begin_time > " + current + " and room_id=" + id
        print(sql)
        # Execute SQL statement
        cur.execute(sql)
        # save search result in a variable and convert it to string
        res = cur.fetchall()
        title = ["id", "user_id", "room_id", "category_id", "price", "weak_time", "need_weak", "begin_time", "end_time", "username", "mobile", "category_name","room_descp","status"]
        # return the string
        return get_list_by_title(res, title)

def get_status2_by_room(id, current):
    with UseDatebase(dbconfig) as cur:
        # Splicing and executing SQL statements
        sql = "SELECT * FROM `order` WHERE begin_time < " + current + " and end_time > "+current +" and room_id=" + id
        print(sql)
        # Execute SQL statement
        cur.execute(sql)
        # save search result in a variable and convert it to string
        res = cur.fetchall()
        title = ["id", "user_id", "room_id", "category_id", "price", "weak_time", "need_weak", "begin_time", "end_time", "username", "mobile", "category_name","room_descp","status"]
        # return the string
        return get_list_by_title(res, title)

def get_status3_by_room(id, current):
    with UseDatebase(dbconfig) as cur:
        # Splicing and executing SQL statements
        sql = "SELECT * FROM `order` WHERE end_time < " + current + " and room_id=" + id
        print(sql)
        # Execute SQL statement
        cur.execute(sql)
        # save search result in a variable and convert it to string
        res = cur.fetchall()
        title = ["id", "user_id", "room_id", "category_id", "price", "weak_time", "need_weak", "begin_time", "end_time", "username", "mobile", "category_name","room_descp","status"]
        # return the string
        return get_list_by_title(res, title)

def get_order_by_id(id):
    with UseDatebase(dbconfig) as cur:
        # Splicing and executing SQL statements
        sql = "SELECT * FROM `order` WHERE id=\"" + id + "\""
        print(sql)
        # Execute SQL statement
        cur.execute(sql)
        # save search result in a variable and convert it to string
        res = cur.fetchall()
        title = ["id", "user_id", "room_id", "category_id", "price", "weak_time", "need_weak", "begin_time", "end_time", "username", "mobile", "category_name","room_descp","status"]
        # return the string
        return get_dict_by_title(res, title)

def get_all_order_by_roomid(id):
    with UseDatebase(dbconfig) as cur:
        # Splicing and executing SQL statements
        sql = "SELECT * FROM `order` WHERE room_id=\"" + id + "\""
        print(sql)
        # Execute SQL statement
        cur.execute(sql)
        # save search result in a variable and convert it to string
        res = cur.fetchall()
        title = ["id", "user_id", "room_id", "category_id", "price", "weak_time", "need_weak", "begin_time", "end_time", "username", "mobile", "category_name","room_descp","status"]
        # return the string
        return get_list_by_title(res, title)


def update_order_back_by_id(id, end_time, status):
    with UseDatebase(dbconfig) as cur:
        # Splicing and executing SQL statements
        sql = "UPDATE `order` set end_time=%s,status=%s WHERE id=%s" % (end_time, status, id)
        print(sql)
        # Execute SQL statement
        cur.execute(sql)
        # save search result in a variable and convert it to string
        res = cur.fetchall()
        # return the string
        return "ok"

def insert_order_ex(data):
    with UseDatebase(dbconfig) as cur:
        # Splicing and executing SQL statements
        print(data)
        sql = 'insert into `order_extra`(order_id, name, price, number, total) values(%s,%s,%s,%s,%s);'
        print(sql)
        try:
            # Execute SQL statement
            res = cur.executemany(sql, data)

        except Exception as e:
            print(e)
            print("wrong database cur")
            return False
        else:

            print("success!")
            return True


def get_all_kefang():
    with UseDatebase(dbconfig) as cur:
        # Splicing and executing SQL statements
        sql = "SELECT SUM(`money`) FROM `order_money` WHERE source=2 and status=1"
        print(sql)
        # Execute SQL statement
        cur.execute(sql)
        # save search result in a variable and convert it to string
        res = cur.fetchall()
        # title = ["id", "order_id", "money", "category_id", "price", "weak_time", "need_weak", "begin_time", "end_time", "username", "mobile", "category_name","room_descp","status"]
        # return the string
        return res

def get_all_ding():
    with UseDatebase(dbconfig) as cur:
        # Splicing and executing SQL statements
        sql = "SELECT SUM(`money`) FROM `order_money` WHERE source=1 and status=1"
        print(sql)
        # Execute SQL statement
        cur.execute(sql)
        # save search result in a variable and convert it to string
        res = cur.fetchall()
        # title = ["id", "order_id", "money", "category_id", "price", "weak_time", "need_weak", "begin_time", "end_time", "username", "mobile", "category_name","room_descp","status"]
        # return the string
        return res

def get_all_ex():
    with UseDatebase(dbconfig) as cur:
        # Splicing and executing SQL statements
        sql = "SELECT SUM(`total`) FROM `order_extra`"
        print(sql)
        # Execute SQL statement
        cur.execute(sql)
        # save search result in a variable and convert it to string
        res = cur.fetchall()
        # title = ["id", "order_id", "money", "category_id", "price", "weak_time", "need_weak", "begin_time", "end_time", "username", "mobile", "category_name","room_descp","status"]
        # return the string
        return res

def get_all_room_order_count():
    with UseDatebase(dbconfig) as cur:
        # Splicing and executing SQL statements
        sql = "SELECT  category_id, count(*) from `order` group by category_id order by count(*) desc;"
        print(sql)
        # Execute SQL statement
        cur.execute(sql)
        # save search result in a variable and convert it to string
        res = cur.fetchall()
        title = ["room_id", "count"]
        # return the string
        return get_list_by_title(res, title)

def insert_order_money(data):
    with UseDatebase(dbconfig) as cur:
        # Splicing and executing SQL statements
        print(data)
        sql = 'insert into `order_money`(order_id, money, source, status) values(%s,%s,%s,%s);'
        print(sql)
        try:
            # Execute SQL statement
            res = cur.executemany(sql, data)

        except Exception as e:
            print(e)
            print("wrong database cur")
            return False
        else:

            print("success!")
            return True

def get_order_by_bengin_and_end(begin, end):
    with UseDatebase(dbconfig) as cur:
        # Splicing and executing SQL statements
        sql = "SELECT * FROM `order` WHERE end_time>=%s and end_time <=%s" % (begin, end)
        print(sql)
        # Execute SQL statement
        cur.execute(sql)
        # save search result in a variable and convert it to string
        res = cur.fetchall()
        title = ["id", "user_id", "room_id", "category_id", "price", "weak_time", "need_weak", "begin_time", "end_time", "username", "mobile", "category_name","room_descp","status"]
        # return the string
        return get_list_by_title(res, title)