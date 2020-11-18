from flask import Flask
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)

app.secret_key="\xbd\xa6\x1f\x9d\xa3\xde\x17\xe4\x0c\xdb\xeb\x82"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/app1?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app=app)
admin = Admin(app=app, name="QUẢN LÝ BÁN VÉ MÁY BAY", template_mode="bootstrap4")

login = LoginManager(app=app)

