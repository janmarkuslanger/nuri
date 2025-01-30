from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from nuri.models import User

view = Blueprint("auth", __name__)


@view.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("home.index"))
        else:
            flash("Invalid email or password.")

    return render_template("auth/login.html")


@view.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
