from flask import render_template, redirect, request
from BanVe2 import app, login
from BanVe2.models import User
from flask_login import login_user, login_required
import hashlib


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/login-admin", methods=["GET", "POST"])
def login_admin():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password", "")
        password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())
        user = User.query.filter(User.user_name == username.strip(),
                                 User.user_password == password).first()

        if user:
            login_user(user=user)
    return redirect("/admin")

@login.user_loader
def user_load(user_id):
    return User.query.get(user_id)

if __name__ == '__main__':
    app.run(debug=True)




