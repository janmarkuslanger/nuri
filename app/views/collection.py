from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Collection, Role
from app.extensions import db
from app.views.auth import roles_required

view = Blueprint("collection", __name__)


@view.route("/", methods=["GET"])
@roles_required(Role.EDITOR, Role.ADMIN)
def index():
    collections = Collection.query.all()
    return render_template("collection/index.html", collections=collections)


@view.route("/create", methods=["GET", "POST"])
@roles_required(Role.EDITOR, Role.ADMIN)
def create():
    if request.method == "POST":
        name = request.form.get("name")
        alias = request.form.get("alias")
        description = request.form.get("description")

        excistingAlias = Collection.query.filter_by(alias=alias).first()
        if excistingAlias:
            flash("Alias already exists", "error")
            return redirect(url_for("collection.index"))

        if name and alias:
            new_collection = Collection(name=name, alias=alias, description=description)
            new_collection.save()
            return redirect(url_for("collection.index"))

    return render_template("collection/create_or_edit.html")


@view.route("/edit/<int:id>", methods=["GET", "POST"])
@roles_required(Role.EDITOR, Role.ADMIN)
def edit(id):
    collection = Collection.query.get_or_404(id)

    if request.method == "POST":
        name = request.form.get("name")
        alias = request.form.get("alias")
        description = request.form.get("description")

        existing_alias = Collection.query.filter(
            Collection.alias == alias, Collection.id != id
        ).first()
        if existing_alias:
            flash("Alias already exists", "error")
            return redirect(url_for("collection.edit", id=id))

        if name and alias:
            collection.name = name
            collection.alias = alias
            collection.description = description
            db.session.commit()
            flash("Collection updated successfully!", "success")
            return redirect(url_for("collection.index"))

    return render_template("collection/create_or_edit.html", item=collection)


@view.route("/delete/<int:id>", methods=["GET", "POST"])
@roles_required(Role.EDITOR, Role.ADMIN)
def delete(id):
    collection = Collection.query.get_or_404(id)

    if request.method == "POST":
        collection.delete()
        return redirect(url_for("collection.index"))

    return render_template("collection/delete.html", collection=collection)
