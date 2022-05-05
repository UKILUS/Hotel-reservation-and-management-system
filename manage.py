from flask import Flask
from admin.route_admin import admin
from customer.route_user import user
app = Flask(__name__)
app.secret_key = '!@#$%^&*()11'
app.debug = True

app.register_blueprint(admin)
app.register_blueprint(user)


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port='9999')
