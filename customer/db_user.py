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


# ==========================================================================
