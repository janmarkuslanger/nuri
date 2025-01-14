from flask import Blueprint, render_template

view = Blueprint("home", __name__)


@view.route("/", methods=["GET"])
def index():
    return render_template("home.html")
