from flask import Blueprint, render_template, request, redirect, url_for
from app.models.collection import Collection
from app import db

view = Blueprint("collection", __name__)

@view.route("/", methods=["GET"])
def list_collections():
    collections = Collection.query.all()
    return render_template("list_collections.html", collections=collections)

@view.route("/create", methods=["GET", "POST"])
def create_collection():
    if request.method == "POST":
        name = request.form.get("name")
        description = request.form.get("description")
        if name:
            new_collection = Collection(name=name, description=description)
            new_collection.save()
            return redirect(url_for("collection.list_collections"))
    return render_template("create_collection.html")
