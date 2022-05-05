import pymysql
from db_use import UseDatebase
from utils import *

dbconfig = {'host': 'localhost',
            'user': 'root',
            'passwd': '19991119',
            'db': 'tuzi-hotel', }

# LHZ
# For login(sign-in) Page
def login_select_email(email):
    with UseDatebase(dbconfig) as cur:
        # Splicing and executing SQL statements
        email = "SELECT `password` FROM user_info WHERE email =" + "\"" + email + "\""
        # Execute SQL statement
        cur.execute(email)
        # save search result in a variable and convert it to string
        res = cur.fetchall()
        # return the string
        return res

# LHZ
# For login(sign-in) Page
def login_select_username(username, is_admin):
    with UseDatebase(dbconfig) as cur:
        # Splicing and executing SQL statements
        email = "SELECT `password` FROM user_info WHERE username =" + "\"" + username + "\" and is_admin=\"" + is_admin + "\""
        # Execute SQL statement
        cur.execute(email)
        # save search result in a variable and convert it to string
        res = cur.fetchall()
        # return the string
        return res

def login_select_username_reg(username):
    with UseDatebase(dbconfig) as cur:
        # Splicing and executing SQL statements
        email = "SELECT `password` FROM user_info WHERE username =" + "\"" + username + "\" "
        print(email)
        # Execute SQL statement
        cur.execute(email)
        # save search result in a variable and convert it to string
        res = cur.fetchall()
        # return the string
        return res

def insert_user(data):
    with UseDatebase(dbconfig) as cur:
        # Splicing and executing SQL statements
        sql = 'insert into user_info(username, email, mobile, password, is_admin) values(%s,%s,%s,%s,%s);'
        try:
            # Execute SQL statement
            cur.executemany(sql, data)
        except:
            print("wrong database cur")
            return False
        else:

            print("success!")
            return True

def get_all_category():
    with UseDatebase(dbconfig) as cur:
        # Splicing and executing SQL statements
        sql = "SELECT * FROM category"
        # Execute SQL statement
        cur.execute(sql)
        # save search result in a variable and convert it to string
        res = cur.fetchall()
        title = ["id", "name", "img", "price", "descp"]

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

def get_category_by_price(price):
    with UseDatebase(dbconfig) as cur:
        # Splicing and executing SQL statements
        sql = "SELECT * FROM category where price=" + price
        # Execute SQL statement
        cur.execute(sql)
        # save search result in a variable and convert it to string
        res = cur.fetchall()
        title = ["id", "name", "img", "price", "descp"]
        # return the string
        return get_dict_by_title(res, title)


def get_room_by_categoryid(id):
    with UseDatebase(dbconfig) as cur:
        # Splicing and executing SQL statements
        sql = "SELECT * FROM room where category_id=" + "\""+ id +"\"order by name asc"
        # Execute SQL statement
        cur.execute(sql)
        # save search result in a variable and convert it to string
        res = cur.fetchall()
        title = ["id", "orientation", "have_windows", "have_book", "name", "category_id", "descp"]
        # return the string
        return get_list_by_title(res, title)

def get_room_by_search(key):
    with UseDatebase(dbconfig) as cur:
        # Splicing and executing SQL statements
        sql = "SELECT * FROM room where orientation=\"" + key + "\""
        print(sql)
        # Execute SQL statement
        cur.execute(sql)
        # save search result in a variable and convert it to string
        res = cur.fetchall()
        title = ["id", "orientation", "have_windows", "have_book", "name", "category_id", "descp"]
        # return the string
        return get_list_by_title(res, title)

def get_room_by_chao_search(key):
    with UseDatebase(dbconfig) as cur:
        # Splicing and executing SQL statements
        sql = "SELECT * FROM room where orientation=\"" + key + "\""
        print(sql)
        # Execute SQL statement
        cur.execute(sql)
        # save search result in a variable and convert it to string
        res = cur.fetchall()
        title = ["id", "orientation", "have_windows", "have_book", "name", "category_id", "descp"]
        # return the string
        return get_list_by_title(res, title)

def get_category_room_by_chao_search(key, cid):
    with UseDatebase(dbconfig) as cur:
        # Splicing and executing SQL statements
        sql = "SELECT * FROM room where orientation=\"" + key + "\"" + "and category_id=\"" + cid +"\""
        print(sql)
        # Execute SQL statement
        cur.execute(sql)
        # save search result in a variable and convert it to string
        res = cur.fetchall()
        title = ["id", "orientation", "have_windows", "have_book", "name", "category_id", "descp"]
        # return the string
        return get_list_by_title(res, title)

def get_category_room_by_chuang(key, cid):
    with UseDatebase(dbconfig) as cur:
        # Splicing and executing SQL statements
        sql = "SELECT * FROM room where have_windows=\"" + key + "\"" + "and category_id=\"" + cid +"\""
        print(sql)
        # Execute SQL statement
        cur.execute(sql)
        # save search result in a variable and convert it to string
        res = cur.fetchall()
        title = ["id", "orientation", "have_windows", "have_book", "name", "category_id", "descp"]
        # return the string
        return get_list_by_title(res, title)

def get_room_by_chuang(key):
    with UseDatebase(dbconfig) as cur:
        # Splicing and executing SQL statements
        sql = "SELECT * FROM room where have_windows=\"" + key + "\""
        print(sql)
        # Execute SQL statement
        cur.execute(sql)
        # save search result in a variable and convert it to string
        res = cur.fetchall()
        title = ["id", "orientation", "have_windows", "have_book", "name", "category_id", "descp"]
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

def get_user_by_email(email):
    with UseDatebase(dbconfig) as cur:
        # Splicing and executing SQL statements
        sql = "SELECT * FROM user_info where email=\"" + email + "\""
        print(email)
        print(sql)
        # Execute SQL statement
        cur.execute(sql)
        # save search result in a variable and convert it to string
        res = cur.fetchall()
        title = ["id", "username", "email", "password", "mobile", "is_admin"]
        # return the string
        return get_dict_by_title(res, title)

def get_user_by_id(id):
    with UseDatebase(dbconfig) as cur:
        # Splicing and executing SQL statements
        sql = "SELECT * FROM user_info where id=\"" + id + "\""
        print(id)
        print(sql)
        # Execute SQL statement
        cur.execute(sql)
        # save search result in a variable and convert it to string
        res = cur.fetchall()
        title = ["id", "username", "email", "password", "mobile", "is_admin"]
        # return the string
        return get_dict_by_title(res, title)

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


def insert_order(data):
    with UseDatebase(dbconfig) as cur:
        # Splicing and executing SQL statements
        print(data)
        sql = 'insert into `order`(user_id, room_id, category_id, price, weak_time, need_weak, begin_time, end_time, username, mobile, category_name, room_descp ) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);'
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

def max_order_id():
    with UseDatebase(dbconfig) as cur:
        # Splicing and executing SQL statements
        sql = 'SELECT MAX(id) from `order`'
        print(sql)
        try:
            # Execute SQL statement
            res = cur.execute(sql)
            last = cur.fetchall()
            last = last[0][0]

        except Exception as e:
            print(e)
            print("wrong database cur")
            return -1
        else:
            if last>0:
                return last
            else:
                return -1


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

def get_all_order_by_user(user_id):
    with UseDatebase(dbconfig) as cur:
        # Splicing and executing SQL statements
        sql = "SELECT * FROM `order` WHERE user_id=\"" + user_id + "\" order by id desc"
        print(sql)
        # Execute SQL statement
        cur.execute(sql)
        # save search result in a variable and convert it to string
        res = cur.fetchall()
        title = ["id", "user_id", "room_id", "category_id", "price", "weak_time", "need_weak", "begin_time", "end_time", "username", "mobile", "category_name","room_descp","status"]
        # return the string
        return get_list_by_title(res, title)

def get_order_ex_sum_by_id(id):
    with UseDatebase(dbconfig) as cur:
        # Splicing and executing SQL statements
        sql = "SELECT SUM(price) FROM `order_extra` WHERE order_id=\"" + id + "\""
        print(sql)
        # Execute SQL statement
        cur.execute(sql)
        # save search result in a variable and convert it to string
        res = cur.fetchall()
        print(res)
        if res[0][0] == None:
            return 0
        else:
            print("订单" + id + "的额外费用" +  res[0][0])
            # return the string
            return res[0][0]

def get_order_money_sum_by_id(id):
    with UseDatebase(dbconfig) as cur:
        # Splicing and executing SQL statements
        sql = "SELECT SUM(money) FROM `order_money` WHERE order_id=\"" + id + "\" and source=1"
        print(sql)
        # Execute SQL statement
        cur.execute(sql)
        # save search result in a variable and convert it to string
        res = cur.fetchall()
        print(res)
        if res[0][0] == None:
            return 0
        else:
            print("定金" + id + "的额外费用" + str(res[0][0]))
            # return the string
            return str(res[0][0])


def update_order_status_by_id(id, mystatus):
    with UseDatebase(dbconfig) as cur:
        # Splicing and executing SQL statements

        print("hahah")
        print(id)
        print(mystatus)
        sql = "UPDATE `order` SET status="+mystatus+" WHERE id=\"" + id + "\""
        print(sql)
        # Execute SQL statement
        cur.execute(sql)
        # save search result in a variable and convert it to string
        res = cur.fetchall()
        # return the string
        return True

def update_order_status_2_by_id(id):
    with UseDatebase(dbconfig) as cur:
        # Splicing and executing SQL statements

        sql = "UPDATE `order` SET status=2 WHERE id=\"" + id + "\""
        print(sql)
        # Execute SQL statement
        cur.execute(sql)
        # save search result in a variable and convert it to string
        res = cur.fetchall()
        # return the string
        return True

def update_end_time_by_id(id, end):
    with UseDatebase(dbconfig) as cur:
        # Splicing and executing SQL statements
        sql = "UPDATE `order` SET end_time="+end+" WHERE id=\"" + id + "\""
        print(sql)
        # Execute SQL statement
        cur.execute(sql)
        # save search result in a variable and convert it to string
        res = cur.fetchall()
        # return the string
        return True

def update_order_delete_by_id(id, stamp):
    with UseDatebase(dbconfig) as cur:
        # Splicing and executing SQL statements
        sql = "UPDATE `order` SET status=-1, end_time="+stamp+"  WHERE id=\"" + id + "\""
        print(sql)
        # Execute SQL statement
        cur.execute(sql)
        # save search result in a variable and convert it to string
        res = cur.fetchall()
        # return the string
        return True

def update_order_money_delete_by_id(id):
    with UseDatebase(dbconfig) as cur:
        # Splicing and executing SQL statements
        sql = "UPDATE `order_money` SET status=-1  WHERE order_id=\"" + id + "\""
        print(sql)
        # Execute SQL statement
        cur.execute(sql)
        # save search result in a variable and convert it to string
        res = cur.fetchall()
        # return the string
        return True

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

def get_can_order_status_by_room(id):
    with UseDatebase(dbconfig) as cur:
        # Splicing and executing SQL statements
        sql = "SELECT * FROM `order` WHERE status=1 and room_id=" + id
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



def update_user__by_id(uid, mobile, email):
    with UseDatebase(dbconfig) as cur:
        # Splicing and executing SQL statements

        print("hahah")
        print(uid)
        print(mobile)
        print(email)
        sql = "UPDATE `user_info` SET mobile='"+mobile+"',email='"+email+"' WHERE id=\"" + uid + "\""

        print(sql)
        # Execute SQL statement
        cur.execute(sql)
        # save search result in a variable and convert it to string
        res = cur.fetchall()
        # return the string
        return True
# ==========================================================================
