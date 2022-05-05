# Project Name: KIKI_Bakery_Online_Sale_System
# Author: LHZ(Liu Haozhe),JMY(Jiang Menyu),LXY(Liang Xinyu),XZY(Xu Zhuoyi)
# Start Date: 2020-10-23
# Last Fix Date: 2020-11-06 16:29
# Windows is can't open "0.0.0.0" on browser, please user ip address or "127.0.0.1"

# Introduce a part of flash module which in use
from flask import Flask, render_template, make_response, request, Response, redirect, url_for
from werkzeug.utils import redirect

# The module to connect python to mysql
import pymysql

# All database statements used by the program which custom
from db_reg import indb, indb_product, login_select, user_select, email_select, password_select, \
    del_user, goods_search, alt_user, select_product, indb_cart, cart_email, cart_product_id, cart_product_name, \
    cart_product_cost


from datetime import datetime
import random

# initialization
app = Flask(__name__)


# LHZ Main page of website
@app.route('/', methods=['GET', 'POST'])
def homepage():
    # Get the cookies from user's browser
    email = request.cookies.get('email')

    # If user have the right cookies
    if email:
        if email == "admin@kiki-group.top":
            name = "You are Administrator"  # if user haven't login set this
            My_Order = ""
            All_Products = ""
            Shopping_Cart = ""
            disabled = "disabled = disabled"
            order = "#"
            cart = "#"
            product = "#"

        else:
            # Set some web page variables
            name = email  # This is user's email
            My_Order = "My Order"
            All_Products = "All Products"
            Shopping_Cart = "Shopping Cart"
            disabled = ""
            order = "order"
            cart = "cart"
            product = "L"

    # If user haven't the right cookies
    else:
        # Set some web page variables
        name = "Not logged in"  # if user haven't login set this
        My_Order = ""
        All_Products = ""
        Shopping_Cart = ""
        disabled = "disabled = disabled"
        order = "#"
        cart = "#"
        product = "#"

    # Define the web page template and pass in variables
    return render_template('mainpage-lhz.html', name=name, My_Order=My_Order, All_Products=All_Products,
                           Shopping_Cart=Shopping_Cart, disabled=disabled, order=order, cart=cart, L=product)


# LHZ To exit account
@app.route('/exit', methods=['GET', 'POST'])
def clear_account():
    # Define the web page template to exit_account page and pass in variables
    # Create a new object
    res = Response(render_template('exit_acount.html'))
    # Delete the cookie that meets the requirements, thus prompting the user to exit the account
    res.delete_cookie('email')
    return res


# LHZ Go To the admin choose page
@app.route('/admin-in', methods=['GET', 'POST'])
def admin_page():
    # Define the web page template to switch_admin page
    return render_template('switch_admin.html')


# LHZ Go To the user_account manage page
@app.route('/admin-user', methods=['GET', 'POST'])
def user_admin():
    # to get all user's user name from database and save them in a list
    user = list(user_select())
    # to get all user's email from database and save them in a list
    email = list(email_select())
    # to get all user's password from database and save them in a list
    password = list(password_select())
    # Get Data from web page
    delete = request.form.get('delete')
    # Get Data from web page
    c_email = request.form.get('change_email')
    # Get Data from web page
    c_password = request.form.get('change_password')

    # When the POST method is received (the user submits the form)
    if request.method == 'POST':
        if alt_user(str(c_email), str(c_password)):
            tip = "Please click reload to Refresh Page"
        else:
            tip = "Operation False"

        if del_user(str(delete)):
            tip = "Please click reload to Refresh Page"
        else:
            tip = "Operation False"
        return render_template('user_management.html', userlist=user, emaillist=email, passwordlist=password, tip=tip)
    return render_template('user_management.html', userlist=user, emaillist=email, passwordlist=password)


# LHZ To show the search_result page
@app.route('/results', methods=['GET', 'POST'])
def do_search():
    # When user Submitted
    if request.method == 'POST':
        # save the Submitted thing in a variable
        phrase = request.form['phrase']
    # when the variable is not empty
    if phrase:
        # Use database to search the result
        searchresult = goods_search(phrase)
        # return the result and jump to the search result page
        return render_template('search_results.html', searchresult=searchresult)


# LHZ:User input email and password to login
@app.route('/login', methods=['GET', 'POST'])
def login():
    # to set the cookie
    resp = make_response(render_template('YES.html'))
    resp_admin = make_response(render_template('jump_user_admin_t.html'))
    # When user Submitted
    if request.method == 'POST':
        # var to save the email form user input

        email = request.form.get('email')
        # var to save the password form user input
        password = request.form.get('password')

        # background log
        print(email)
        print(password)

        # to change the var type to string
        email = str(email)
        print(email)

        # In the comparison method, the user input data (user name + password) are connected together and compared with the tuple after slicing
        passwd = str(login_select(email))[3:-5]
        print(passwd)

        # when the user input the admin user email
        if email == "admin@kiki-group.top":
            if str(passwd) == password:
                # set cookie and The expiration time is two days
                resp_admin.set_cookie("email", email, max_age=172800)
                return resp_admin
        # when the user other email
        elif email != "admin@kiki-group.top":
            if str(passwd) == password:
                # set cookie and The expiration time is two days
                resp.set_cookie("email", email, max_age=172800)
                return resp
        # when Login failed jump to the warring page
        else:
            return render_template('NO.html')
    return render_template('sign-in.html')


# LHZ
# Register new user
@app.route('/register', methods=['GET', 'POST'])
def start():
    # When user Submitted
    if request.method == 'POST':
        # Get User name
        username = request.form['username']
        # Get User email
        email = request.form['email']
        # Get User password
        password = request.form['password']
        # Save it to a list
        data = [
            (username, email, password),
        ]
        # save in database
        indb(data)
        # Go back to main page
        return render_template('mainpage-lhz.html')
    return render_template('register.html')


# JMY :
# Jump to all items list page
@app.route('/L', methods=['GET', 'POST'])
def l():
    # Jump to Product-list.html
    return render_template('Product-list.html')


# JMY :
# Jump to chocolate items list page
@app.route('/L1', methods=['GET', 'POST'])
def l1():
    # Jump to Product-list-1.html
    return render_template('Product-list-1.html')


# JMY :
# Jump to nut items list page
@app.route('/L2', methods=['GET', 'POST'])
def l2():
    # Jump to Product-list-2.html
    return render_template('Product-list-2.html')


# JMY :
# Jump to coffee items list page
@app.route('/L3', methods=['GET', 'POST'])
def l3():
    # Jump to Product-list-3.html
    return render_template('Product-list-3.html')


# JMY :
# Jump to ice-cream items list page
@app.route('/L4', methods=['GET', 'POST'])
def l4():
    # Jump to Product-list-4.html
    return render_template('Product-list-4.html')


# JMY :
# Send product_id is 1 to the select_product function, the query results are transferred to the html page
# Where pn is product_id = 1 product's name; pc is this product cost; pin is this product information
@app.route('/P1', methods=['GET', 'POST'])
def P1():
    # Send a request with product_id 1 to the product search method
    pp = select_product('1')
    # Attach the first product name of the returned data to pn
    pn = pp[0]
    # Remove unnecessary characters
    pn = str(pn)[3:-5]
    # Attach the second product cost of the returned data to pn
    pc = pp[1]
    # Remove unnecessary characters
    pc = str(pc)[11:-6]
    # Attach the third product information of the returned data to pn
    pin = pp[2]
    # Remove unnecessary characters
    pin = str(pin)[3:-5]
    # With the useful string extracted from the function, jump to the product details page
    return render_template('P1.html', pn=pn, pc=pc, pin=pin)


# JMY
# Send product_id is 2 to the select_product function, the query results are transferred to the html page
# Where pn is product_id = 2 product's name; pc is this product cost; pin is this product information
@app.route('/P2', methods=['GET', 'POST'])
def P2():
    # Send a request with product_id 2 to the product search method
    pp = select_product('2')
    # Attach the first product name of the returned data to pn
    pn = pp[0]
    # Remove unnecessary characters
    pn = str(pn)[3:-5]
    # Attach the second product cost of the returned data to pn
    pc = pp[1]
    # Remove unnecessary characters
    pc = str(pc)[11:-6]
    # Attach the third product information of the returned data to pn
    pin = pp[2]
    # Remove unnecessary characters
    pin = str(pin)[3:-5]
    # With the useful string extracted from the function, jump to the product details page
    return render_template('P2.html', pn=pn, pc=pc, pin=pin)


# JMY
# Send product_id is 3 to the select_product function, the query results are transferred to the html page
# Where pn is product_id = 3 product's name; pc is this product cost; pin is this product information
@app.route('/P3', methods=['GET', 'POST'])
def P3():
    # Send a request with product_id 3 to the product search method
    pp = select_product('3')
    # Attach the first product name of the returned data to pn
    pn = pp[0]
    # Remove unnecessary characters
    pn = str(pn)[3:-5]
    # Attach the second product cost of the returned data to pn
    pc = pp[1]
    # Remove unnecessary characters
    pc = str(pc)[11:-6]
    # Attach the third product information of the returned data to pn
    pin = pp[2]
    # Remove unnecessary characters
    pin = str(pin)[3:-5]
    # With the useful string extracted from the function, jump to the product details page
    return render_template('P3.html', pn=pn, pc=pc, pin=pin)


# JMY
# Send product_id is 4 to the select_product function, the query results are transferred to the html page
# Where pn is product_id = 4 product's name; pc is this product cost; pin is this product information
@app.route('/P4', methods=['GET', 'POST'])
def P4():
    # Send a request with product_id 4 to the product search method
    pp = select_product('4')
    # Attach the first product name of the returned data to pn
    pn = pp[0]
    # Remove unnecessary characters
    pn = str(pn)[3:-5]
    # Attach the second product cost of the returned data to pn
    pc = pp[1]
    # Remove unnecessary characters
    pc = str(pc)[11:-6]
    # Attach the third product information of the returned data to pn
    pin = pp[2]
    # Remove unnecessary characters
    pin = str(pin)[3:-5]
    # With the useful string extracted from the function, jump to the product details page
    return render_template('P4.html', pn=pn, pc=pc, pin=pin)


# JMY
# Send product_id is 5 to the select_product function, the query results are transferred to the html page
# Where pn is product_id = 5 product's name; pc is this product cost; pin is this product information
@app.route('/P5', methods=['GET', 'POST'])
def P5():
    # Send a request with product_id 5 to the product search method
    pp = select_product('5')
    # Attach the first product name of the returned data to pn
    pn = pp[0]
    # Remove unnecessary characters
    pn = str(pn)[3:-5]
    # Attach the second product cost of the returned data to pn
    pc = pp[1]
    # Remove unnecessary characters
    pc = str(pc)[11:-6]
    # Attach the third product information of the returned data to pn
    pin = pp[2]
    # Remove unnecessary characters
    pin = str(pin)[3:-5]
    # With the useful string extracted from the function, jump to the product details page
    return render_template('P5.html', pn=pn, pc=pc, pin=pin)


# JMY
# Send product_id is 6 to the select_product function, the query results are transferred to the html page
# Where pn is product_id = 6 product's name; pc is this product cost; pin is this product information
@app.route('/P6', methods=['GET', 'POST'])
def P6():
    # Send a request with product_id 6 to the product search method
    pp = select_product('6')
    # Attach the first product name of the returned data to pn
    pn = pp[0]
    # Remove unnecessary characters
    pn = str(pn)[3:-5]
    # Attach the second product cost of the returned data to pn
    pc = pp[1]
    # Remove unnecessary characters
    pc = str(pc)[11:-6]
    # Attach the third product information of the returned data to pn
    pin = pp[2]
    # Remove unnecessary characters
    pin = str(pin)[3:-5]
    # With the useful string extracted from the function, jump to the product details page
    return render_template('P6.html', pn=pn, pc=pc, pin=pin)


# JMY
# Send product_id is 7 to the select_product function, the query results are transferred to the html page
# Where pn is product_id = 7 product's name; pc is this product cost; pin is this product information
@app.route('/P7', methods=['GET', 'POST'])
def P7():
    # Send a request with product_id 7 to the product search method
    pp = select_product('7')
    # Attach the first product name of the returned data to pn
    pn = pp[0]
    # Remove unnecessary characters
    pn = str(pn)[3:-5]
    # Attach the second product cost of the returned data to pn
    pc = pp[1]
    # Remove unnecessary characters
    pc = str(pc)[11:-6]
    # Attach the third product information of the returned data to pn
    pin = pp[2]
    # Remove unnecessary characters
    pin = str(pin)[3:-5]
    # With the useful string extracted from the function, jump to the product details page
    return render_template('P7.html', pn=pn, pc=pc, pin=pin)


# JMY
# Send product_id is 8 to the select_product function, the query results are transferred to the html page
# Where pn is product_id = 8 product's name; pc is this product cost; pin is this product information
@app.route('/P8', methods=['GET', 'POST'])
def P8():
    # Send a request with product_id 8 to the product search method
    pp = select_product('8')
    # Attach the first product name of the returned data to pn
    pn = pp[0]
    # Remove unnecessary characters
    pn = str(pn)[3:-5]
    # Attach the second product cost of the returned data to pn
    pc = pp[1]
    # Remove unnecessary characters
    pc = str(pc)[11:-6]
    # Attach the third product information of the returned data to pn
    pin = pp[2]
    # Remove unnecessary characters
    pin = str(pin)[3:-5]
    # With the useful string extracted from the function, jump to the product details page
    return render_template('P8.html', pn=pn, pc=pc, pin=pin)


# JMY
# Send product_id is 9 to the select_product function, the query results are transferred to the html page
# Where pn is product_id = 9 product's name; pc is this product cost; pin is this product information
@app.route('/P9', methods=['GET', 'POST'])
def P9():
    # Send a request with product_id 9 to the product search method
    pp = select_product('9')
    # Attach the first product name of the returned data to pn
    pn = pp[0]
    # Remove unnecessary characters
    pn = str(pn)[3:-5]
    # Attach the second product cost of the returned data to pn
    pc = pp[1]
    # Remove unnecessary characters
    pc = str(pc)[11:-6]
    # Attach the third product information of the returned data to pn
    pin = pp[2]
    # Remove unnecessary characters
    pin = str(pin)[3:-5]
    # With the useful string extracted from the function, jump to the product details page
    return render_template('P9.html', pn=pn, pc=pc, pin=pin)


# JMY
# Send product_id is 10 to the select_product function, the query results are transferred to the html page
# Where pn is product_id = 10 product's name; pc is this product cost; pin is this product information
@app.route('/P10', methods=['GET', 'POST'])
def P10():
    # Send a request with product_id 10 to the product search method
    pp = select_product('10')
    # Attach the first product name of the returned data to pn
    pn = pp[0]
    # Remove unnecessary characters
    pn = str(pn)[3:-5]
    # Attach the second product cost of the returned data to pn
    pc = pp[1]
    # Remove unnecessary characters
    pc = str(pc)[11:-6]
    # Attach the third product information of the returned data to pn
    pin = pp[2]
    # Remove unnecessary characters
    pin = str(pin)[3:-5]
    # With the useful string extracted from the function, jump to the product details page
    return render_template('P10.html', pn=pn, pc=pc, pin=pin)


# JMY
# Send product_id is 11 to the select_product function, the query results are transferred to the html page
# Where pn is product_id = 11 product's name; pc is this product cost; pin is this product information
@app.route('/P11', methods=['GET', 'POST'])
def P11():
    # Send a request with product_id 11 to the product search method
    pp = select_product('11')
    # Attach the first product name of the returned data to pn
    pn = pp[0]
    # Remove unnecessary characters
    pn = str(pn)[3:-5]
    # Attach the second product cost of the returned data to pn
    pc = pp[1]
    # Remove unnecessary characters
    pc = str(pc)[11:-6]
    # Attach the third product information of the returned data to pn
    pin = pp[2]
    # Remove unnecessary characters
    pin = str(pin)[3:-5]
    # With the useful string extracted from the function, jump to the product details page
    return render_template('P11.html', pn=pn, pc=pc, pin=pin)


# JMY
# Send product_id is 12 to the select_product function, the query results are transferred to the html page
# Where pn is product_id = 12 product's name; pc is this product cost; pin is this product information
@app.route('/P12', methods=['GET', 'POST'])
def P12():
    # Send a request with product_id 12 to the product search method
    pp = select_product('12')
    # Attach the first product name of the returned data to pn
    pn = pp[0]
    # Remove unnecessary characters
    pn = str(pn)[3:-5]
    # Attach the second product cost of the returned data to pn
    pc = pp[1]
    # Remove unnecessary characters
    pc = str(pc)[11:-6]
    # Attach the third product information of the returned data to pn
    pin = pp[2]
    # Remove unnecessary characters
    pin = str(pin)[3:-5]
    # With the useful string extracted from the function, jump to the product details page
    return render_template('P12.html', pn=pn, pc=pc, pin=pin)


# JMY
# Send product_id is 13 to the select_product function, the query results are transferred to the html page
# Where pn is product_id = 13 product's name; pc is this product cost; pin is this product information
@app.route('/P13', methods=['GET', 'POST'])
def P13():
    # Send a request with product_id 13 to the product search method
    pp = select_product('13')
    # Attach the first product name of the returned data to pn
    pn = pp[0]
    # Remove unnecessary characters
    pn = str(pn)[3:-5]
    # Attach the second product cost of the returned data to pn
    pc = pp[1]
    # Remove unnecessary characters
    pc = str(pc)[11:-6]
    # Attach the third product information of the returned data to pn
    pin = pp[2]
    # Remove unnecessary characters
    pin = str(pin)[3:-5]
    # With the useful string extracted from the function, jump to the product details page
    return render_template('P13.html', pn=pn, pc=pc, pin=pin)


# LXY
# When jumping to the CC1 page, get the current user login information and the product ID that the user needs to buy into the data.
@app.route('/CC1/<id>', methods=['GET', 'POST'])
def CC1(id):

    return render_template('CC1.html')




# LXY
# When jumping to the CC2 page, get the current user login information and the product ID that the user needs to buy into the data.
@app.route('/CC2', methods=['GET', 'POST'])
def CC2():
    # Request Cokkies to get the email and name it Email
    email = request.cookies.get('email')
    # Make the product_ID value 2.
    product_id = ['2']
    # Define a data and store the email and product_ID in the list.
    data = [
        (email, product_id),
    ]
    # Call the function indb_CART and pass in data as an argument
    indb_cart(data)
    # Return the render_template function to access and directly render CC2.html

    return render_template('CC2.html')


# LXY
# When jumping to the CC3 page, get the current user login information and the product ID that the user needs to buy into the data.
@app.route('/CC3', methods=['GET', 'POST'])
def CC3():
    # Request Cokkies to get the email and name it Email
    email = request.cookies.get('email')
    # Make the product_ID value 3.
    product_id = ['3']
    # Define a data and store the email and product_ID in the list.
    data = [
        (email, product_id),
    ]
    # Call the function indb_CART and pass in data as an argument
    indb_cart(data)
    # Return the render_template function to access and directly render CC3.html

    return render_template('CC3.html')


# LXY
# When jumping to the CC4 page, get the current user login information and the product ID that the user needs to buy into the data.
@app.route('/CC4', methods=['GET', 'POST'])
def CC4():
    # Request Cokkies to get the email and name it Email
    email = request.cookies.get('email')
    # Make the product_ID value 4.
    product_id = ['4']
    # Define a data and store the email and product_ID in the list.
    data = [
        (email, product_id),
    ]
    # Call the function indb_CART and pass in data as an argument
    indb_cart(data)
    # Return the render_template function to access and directly render CC4.html

    return render_template('CC4.html')


# LXY
# When jumping to the CC5 page, get the current user login information and the product ID that the user needs to buy into the data.
@app.route('/CC5', methods=['GET', 'POST'])
def CC5():
    # Request Cokkies to get the email and name it Email
    email = request.cookies.get('email')
    # Make the product_ID value 5.
    product_id = ['5']
    # Define a data and store the email and product_ID in the list.
    data = [
        (email, product_id),
    ]
    # Call the function indb_CART and pass in data as an argument
    indb_cart(data)
    # Return the render_template function to access and directly render CC5.html

    return render_template('CC5.html')


# LXY
# When jumping to the CC6 page, get the current user login information and the product ID that the user needs to buy into the data.
@app.route('/CC6', methods=['GET', 'POST'])
def CC6():
    # Request Cokkies to get the email and name it Email
    email = request.cookies.get('email')
    # Make the product_ID value 6.

    product_id = ['6']
    # Define a data and store the email and product_ID in the list.
    data = [
        (email, product_id),
    ]
    # Call the function indb_CART and pass in data as an argument
    indb_cart(data)
    # Return the render_template function to access and directly render CC6.html

    return render_template('CC6.html')


# LXY
# When jumping to the CC7 page, get the current user login information and the product ID that the user needs to buy into the data.
@app.route('/CC7', methods=['GET', 'POST'])
def CC7():
    # Request Cokkies to get the email and name it Email
    email = request.cookies.get('email')
    # Make the product_ID value 7.
    product_id = ['7']
    # Define a data and store the email and product_ID in the list.
    data = [
        (email, product_id),
    ]
    # Call the function indb_CART and pass in data as an argument
    indb_cart(data)
    # Return the render_template function to access and directly render CC7.html

    return render_template('CC7.html')


# LXY
# When jumping to the CC8 page, get the current user login information and the product ID that the user needs to buy into the data.
@app.route('/CC8', methods=['GET', 'POST'])
def CC8():
    # Request Cokkies to get the email and name it Email
    email = request.cookies.get('email')
    # Make the product_ID value 8.
    product_id = ['8']
    # Define a data and store the email and product_ID in the list.
    data = [
        (email, product_id),
    ]
    # Call the function indb_CART and pass in data as an argument
    indb_cart(data)
    # Return the render_template function to access and directly render CC8.html

    return render_template('CC8.html')


# LXY
# When jumping to the CC9 page, get the current user login information and the product ID that the user needs to buy into the data.
@app.route('/CC9', methods=['GET', 'POST'])
def CC9():
    # Request Cokkies to get the email and name it Email
    email = request.cookies.get('email')
    # Make the product_ID value 9.

    product_id = ['9']
    # Define a data and store the email and product_ID in the list.

    data = [
        (email, product_id),
    ]
    # Call the function indb_CART and pass in data as an argument
    indb_cart(data)
    # Return the render_template function to access and directly render CC9.html

    return render_template('CC9.html')


# LXY
# When jumping to the CC10 page, get the current user login information and the product ID that the user needs to buy into the data.
@app.route('/CC10', methods=['GET', 'POST'])
def CC10():
    # Request Cokkies to get the email and name it Email
    email = request.cookies.get('email')
    # Make the product_ID value 10.
    product_id = ['10']
    # Define a data and store the email and product_ID in the list.
    data = [
        (email, product_id),
    ]
    # Call the function indb_CART and pass in data as an argument
    indb_cart(data)
    # Return the render_template function to access and directly render CC10.html

    return render_template('CC10.html')


# LXY
# When jumping to the CC11 page, get the current user login information and the product ID that the user needs to buy into the data.
@app.route('/CC11', methods=['GET', 'POST'])
def CC11():
    # Request Cokkies to get the email and name it Email
    email = request.cookies.get('email')
    # Make the product_ID value 11.
    product_id = ['11']
    # Define a data and store the email and product_ID in the list.
    data = [
        (email, product_id),
    ]
    # Call the function indb_CART and pass in data as an argument
    indb_cart(data)
    # Return the render_template function to access and directly render CC11.html
    return render_template('CC11.html')


# LXY
# When jumping to the CC12 page, get the current user login information and the product ID that the user needs to buy into the data.
@app.route('/CC12', methods=['GET', 'POST'])
def CC12():
    # Request Cokkies to get the email and name it Email
    email = request.cookies.get('email')
    # Make the product_ID value 12.
    product_id = ['12']
    # Define a data and store the email and product_ID in the list.
    data = [
        (email, product_id),
    ]
    # Call the function indb_CART and pass in data as an argument
    indb_cart(data)
    # Return the render_template function to access and directly render CC12.html
    return render_template('CC12.html')


# LXY
# When jumping to the CC13 page, get the current user login information and the product ID that the user needs to buy into the data.
@app.route('/CC13', methods=['GET', 'POST'])
def CC13():
    # Request Cokkies to get the email and name it Email
    email = request.cookies.get('email')
    # Make the product_ID value 13.
    product_id = ['13']
    # Define a data and store the email and product_ID in the list.
    data = [
        (email, product_id),
    ]
    # Call the function indb_CART and pass in data as an argument
    indb_cart(data)
    # Return the render_template function to access and directly render CC13.html
    return render_template('CC13.html')


# LXY
# When you go to the shopping cart page, get the email of the currently logged in user, and display the current user name and product information required by the user into the current page by calling some functions.
@app.route('/cart', methods=['GET', 'POST'])
def cart():
    # Get the email value from the cookies and define it as aa
    aa = request.cookies.get('email')
    # Define a list named emaill and pass the value into the cart_email method.
    emaill = list(cart_email(aa))
    print(emaill)
    # Define a list named product_idd and pass the value into the cart_product_id method.
    product_idd = list(cart_product_id(aa))
    print(product_idd)
    # Define a list named product_namee and pass the value into the cart_product_name method.
    product_namee = list(cart_product_name(aa))
    print(product_namee)
    # Define a list named product_costt and pass the value into the cart_product_cost method.
    product_costt = cart_product_cost(aa)
    print(product_costt)


    # Return render_template function can renders the static cart1.html file, passes the parameters to the HTML, and makes an HTML display the query email, Peoduct_ID, product_name.product_cost.Information.
    return render_template('cart1.html', emaillist=emaill, productidlist=product_idd, productnamelist=product_namee,
                           productcosttlist=product_costt)

# Run IP & Port
if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port='8888')
