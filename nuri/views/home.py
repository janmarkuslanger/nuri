from flask import Blueprint, render_template
from flask_login import login_required

view = Blueprint("home", __name__)


@view.route("/", methods=["GET"])
@login_required
def index():
    return render_template("home.html")
