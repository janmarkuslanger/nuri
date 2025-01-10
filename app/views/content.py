from flask import Blueprint, render_template, redirect, request, url_for, flash
from app.models import Collection, Content

view = Blueprint("content", __name__)

@view.route("/", methods=["GET"])
def index():
    collections = Collection.query.all()

    return render_template(
        "content/list.html",
        collections=collections,
    )

@view.route("/<int:collection_id>", methods=["GET"])
def index(collection_id):
    collection = Collection.query.get_or_404(collection_id)
    contents = Content.query.filter_by(collection_id=collection_id).all()

    return render_template(
        "content/index.html",
        collection=collection,
        contents=contents
    )

@view.route("/create/<int:collection_id>", methods=["GET", "POST"])
def create_content(collection_id):
    collection = Collection.query.get_or_404(collection_id)
    fields = collection.fields

    if request.method == "POST":
        data = {}
        errors = []

        for field in fields:
            if field.is_list:
                value = request.form.getlist(field.alias)
            else:
                value = request.form.get(field.alias) 


            if field.field_type == "INTEGER":
                if field.is_list:
                    try:
                        value = [int(v) for v in value] 
                    except ValueError:
                        errors.append(f"{field.name} muss eine Liste von Zahlen sein.")
                else:
                    try:
                        value = int(value)
                    except ValueError:
                        errors.append(f"{field.name} muss eine Zahl sein.")
            elif field.field_type == "BOOLEAN":
                value = [v == "on" for v in value] if field.is_list else (value == "on")

            data[field.alias] = value

        if errors:
            flash(" ".join(errors), "error")
        else:
            new_content = Content(collection_id=collection_id, data=data)
            new_content.save()
            flash("Content erfolgreich erstellt!", "success")
            return redirect(url_for("content.list_content", collection_id=collection_id))

    return render_template("content/create.html", collection=collection)
