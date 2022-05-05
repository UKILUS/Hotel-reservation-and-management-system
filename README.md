# 安装项目
- pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

# 初始化数据库
- 初始化tuzu-hotel.sql

# 安装后执行项目
- python manage.py

# 项目说明
- admin是管理员和BOSS后台页面对应的关系，里面db_admin.py是操作管理员数据库的  route_admin是管理员后台的业务逻辑
- cuetomer是用户页面对应的关系，里面db_user.py是操作用户数据库的  route_user是用户的业务逻辑
- mrd是需求文档，可以删除，每次你给我的需求我都整理在这里
- static是静态文件夹，所有的css js都在这里
- templates是HTML文件所在，也就是前端，你需要修改的中文变为英文，修改这里就可以了

- flask_run.py 旧项目文件可以删除
- json_response 是返回json格式的ajax封装，这里主要是后台图表统计数据用到了
- manage.py 是项目执行文件，运行它就可以启动项目了
- utils是公用的工具文件，里面是一些通用的方法




