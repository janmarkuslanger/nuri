from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Collection, Content, FieldType, Field
from app import db

view = Blueprint("content", __name__, url_prefix="/content")


@view.route("/collections", methods=["GET"])
def list_collections():
    collections = Collection.query.all()
    return render_template("content/list.html", collections=collections)


@view.route("/<int:collection_id>", methods=["GET"])
def index(collection_id):
    collection = Collection.query.get_or_404(collection_id)
    contents = Content.query.filter_by(collection_id=collection_id).all()
    return render_template(
        "content/index.html", collection=collection, contents=contents
    )


@view.route("/create/<int:collection_id>", methods=["GET", "POST"])
def create(collection_id):
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

            if field.field_type == FieldType.INTEGER:
                try:
                    value = [int(v) for v in value] if field.is_list else int(value)
                except ValueError:
                    errors.append(f"{field.name} muss eine Zahl sein.")
            elif field.field_type == FieldType.BOOLEAN:
                value = [v == "on" for v in value] if field.is_list else (value == "on")

            data[field.alias] = value

        if errors:
            flash(" ".join(errors), "error")
        else:
            new_content = Content(collection_id=collection_id, data=data)
            new_content.save()
            flash("Content erfolgreich erstellt!", "success")
            return redirect(url_for("content.index", collection_id=collection_id))

    has_collection = any(field.field_type == FieldType.COLLECTION for field in fields)

    all_content = (
        db.session.query(
            Content,
            Collection.name.label("collection_name"),
            Field.alias.label("display_field_alias"),
        )
        .join(Collection, Content.collection_id == Collection.id)
        .outerjoin(
            Field,
            (Field.collection_id == Collection.id) & (Field.display_field == True),
        )
        .all()
        if has_collection
        else None
    )

    return render_template(
        "content/create_or_edit.html",
        collection=collection,
        all_content=all_content,
        FieldType=FieldType,
    )


@view.route("/edit/<int:content_id>", methods=["GET", "POST"])
def edit(content_id):
    content = Content.query.get_or_404(content_id)
    collection = content.collection
    fields = collection.fields

    if request.method == "POST":
        data = {}

        for field in fields:

            if field.is_list:
                value = request.form.getlist(field.alias)
            else:
                value = request.form.get(field.alias)

            if field.field_type == FieldType.NUMBER:
                value = [int(v) for v in value] if field.is_list else int(value)
            elif field.field_type == FieldType.BOOLEAN:
                value = [v == "on" for v in value] if field.is_list else (value == "on")
                
            print(field.alias, value)

            data[field.alias] = value

        content.data = data
        db.session.commit()
        flash("Content erfolgreich bearbeitet!", "success")
        return redirect(url_for("content.index", collection_id=collection.id))

    has_collection = any(field.field_type == FieldType.COLLECTION for field in fields)

    all_content = (
        db.session.query(
            Content,
            Collection.name.label("collection_name"),
            Field.alias.label("display_field_alias"),
        )
        .join(Collection, Content.collection_id == Collection.id)
        .outerjoin(
            Field,
            (Field.collection_id == Collection.id) & (Field.display_field == True),
        )
        .all()
        if has_collection
        else None
    )

    return render_template(
        "content/create_or_edit.html",
        content=content,
        collection=collection,
        all_content=all_content,
        FieldType=FieldType,
    )


@view.route("/delete/<int:content_id>", methods=["POST"])
def delete(content_id):
    content = Content.query.get_or_404(content_id)
    db.session.delete(content)
    db.session.commit()
    flash("Content erfolgreich gelöscht!", "success")
    return redirect(url_for("content.index", collection_id=content.collection_id))
