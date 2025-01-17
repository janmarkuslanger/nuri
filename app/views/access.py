from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Access, Role
from app.views.auth import roles_required


view = Blueprint("access", __name__)


@view.route("/", methods=["GET"])
@roles_required(Role.ADMIN)
def index():
    items = Access.query.all()
    return render_template("access/index.html", items=items)


@view.route("/create", methods=["GET", "POST"])
@roles_required(Role.ADMIN)
def create():
    if request.method == "POST":
        name = request.form.get("name")
        new_item = Access(name=name)
        new_item.generate_api_key()
        new_item.save()
        
        return redirect(url_for("access.index"))
        
    return render_template(
        "access/create.html"
    )

@view.route("/delete/<int:id>", methods=["GET", "POST"])
@roles_required(Role.ADMIN)
def delete(id):
    item = Access.query.get_or_404(id)

    if request.method == "POST":
        item.delete()
        return redirect(url_for("access.index"))

    return render_template("access/delete.html", item=item)
