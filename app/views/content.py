from flask import Blueprint, render_template
from app.models import Collection, Content

view = Blueprint("content", __name__)

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
            value = request.form.get(field.alias)
            if field.field_type == "INTEGER":
                try:
                    value = int(value)
                except ValueError:
                    errors.append(f"{field.name} muss eine Zahl sein.")
            elif field.field_type == "BOOLEAN":
                value = request.form.get(field.alias) == "on"

            data[field.alias] = value

        if errors:
            flash(" ".join(errors), "error")
        else:
            new_content = Content(collection_id=collection_id, data=data)
            new_content.save()
            flash("Content erfolgreich erstellt!", "success")
            return redirect(url_for("content.list_content", collection_id=collection_id))

    return render_template("content/create.html", collection=collection)
