from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.collection import Collection
from app import db

view = Blueprint("collection", __name__)

@view.route("/", methods=["GET"])
def index():
    collections = Collection.query.all()
    return render_template("list_collections.html", collections=collections)

@view.route("/create", methods=["GET", "POST"])
def create_collection():
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
