# Hotel-reservation-and-management-system
3000
# The installation program
- pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
- 
# Initializing the database
-Initialize bunnt-hotel.sql

# Execute the project after installation
- python manage.py

# Project description
- Admin specifies the relationship between the administrator and the BOSS background page.
  db_admin. py specifies the route_admin specifies the service logic of the administrator background
  
- Cuetomer is the relationship between the user's page, where db_user.py is the user's database route_user is the user's business logic

- Static is the static folder where all CSS js are stored

- Templates is where the HTML file is, which is the front end.

- jSON_response is an Ajax wrapper that returns JSON format, which is mainly used for background chart statistics

- manage.py is the project execution file that can be run to start the project

- utils is a public utility file that contains some common methods
