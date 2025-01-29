from flask import Blueprint, render_template, request, redirect, url_for
from nuri.models import Collection, Content, FieldType, Field, Asset
from nuri.extensions import db
from nuri.views.auth import roles_required
from nuri.models.role import Role
from nuri.utils.message import created_success, deleted_success, updated_success, error

view = Blueprint("content", __name__, url_prefix="/content")


@view.route("/collections", methods=["GET"])
@roles_required(Role.EDITOR, Role.ADMIN)
def list_collections():
    collections = Collection.query.all()
    return render_template("content/list.html", collections=collections)


@view.route("/<int:id>", methods=["GET"])
@roles_required(Role.EDITOR, Role.ADMIN)
def index(id):
    # must name it id atm because of the table macro url_for must be customized
    collection_id = id
    collection = Collection.query.get_or_404(collection_id)
    contents = Content.query.filter_by(collection_id=collection_id).all()
    
    return render_template(
        "content/index.html", collection=collection, contents=contents
    )


@view.route("/create/<int:collection_id>", methods=["GET", "POST"])
@roles_required(Role.EDITOR, Role.ADMIN)
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

            if field.field_type == FieldType.NUMBER:
                try:
                    value = [int(v) for v in value] if field.is_list else int(value)
                except ValueError:
                    errors.append(f"{field.name} must be a number.")
            elif field.field_type == FieldType.BOOLEAN:
                value = [v == "on" for v in value] if field.is_list else (value == "on")

            data[field.alias] = value

        if errors:
            error(" ".join(errors))
        else:
            new_content = Content(collection_id=collection_id, data=data)
            new_content.save()
            created_success("Content")
            return redirect(url_for("content.index", id=collection_id))

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

    has_assets = any(field.field_type == FieldType.ASSET for field in fields)

    all_assets = Asset.query.all() if has_assets else None
    
    content_fields = []
    for field in collection.fields:
        template_name = field.field_type.value.lower() if field.field_type.value.lower() in ["asset", "boolean", "collection", "textarea", "richtext"] else "*"
        template_path = "template_fields/" + template_name + ".html"
        rendered = render_template(template_path, field=field, all_content=all_content, all_assets=all_assets, FieldType=FieldType)
        content_fields.append(rendered)

    return render_template(
        "content/create_or_edit.html",
        collection=collection,
        all_content=all_content,
        all_assets=all_assets,
        FieldType=FieldType,
        content_fields=content_fields
    )


@view.route("/edit/<int:content_id>", methods=["GET", "POST"])
@roles_required(Role.EDITOR, Role.ADMIN)
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

            data[field.alias] = value

        content.data = data
        db.session.commit()
        updated_success("Content")
        return redirect(url_for("content.index", id=collection.id))

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

    has_assets = any(field.field_type == FieldType.ASSET for field in fields)

    all_assets = Asset.query.all() if has_assets else None

    content_fields = []
    for field in collection.fields:
        template_name = field.field_type.value.lower() if field.field_type.value.lower() in ["asset", "boolean", "collection", "textarea", "richtext"] else "*"
        template_path = "template_fields/" + template_name + ".html"
        rendered = render_template(template_path, field=field, content=content, all_content=all_content, all_assets=all_assets, FieldType=FieldType)
        content_fields.append(rendered)

    return render_template(
        "content/create_or_edit.html",
        content=content,
        collection=collection,
        all_content=all_content,
        all_assets=all_assets,
        FieldType=FieldType,
        content_fields=content_fields
    )


@view.route("/delete/<int:id>", methods=["GET", "POST"])
@roles_required(Role.EDITOR, Role.ADMIN)
def delete(id):
    content = Content.query.get_or_404(id)

    if request.method == "POST":
        content.delete()
        deleted_success("Content")
        return redirect(url_for("content.list_collections"))

    return render_template("content/delete.html", content=content)
