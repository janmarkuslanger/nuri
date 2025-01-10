from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.collection import Collection
from app import db

view = Blueprint("collection", __name__)


@view.route("/", methods=["GET"])
def index():
    collections = Collection.query.all()
    return render_template("list_collections.html", collections=collections)


@view.route("/create", methods=["GET", "POST"])
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
        
    return render_template("create_collection.html")


@view.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    collection = Collection.query.get_or_404(id)

    if request.method == "POST":
        name = request.form.get("name")
        alias = request.form.get("alias")
        description = request.form.get("description")

        existing_alias = Collection.query.filter(Collection.alias == alias, Collection.id != id).first()
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

    return render_template("edit_collection.html", collection=collection)


@view.route("/delete/<int:id>", methods=["GET", "POST"])
def delete(id):
    collection = Collection.query.get_or_404(id)

    if request.method == "POST":
        collection.delete()
        return redirect(url_for("collection.index"))

    return render_template("delete_collection.html", collection=collection)
