from flask import Blueprint, render_template, request, redirect, url_for
from nuri.models import Field, Collection, FieldType, Role
from nuri.extensions import db
from nuri.views.auth import roles_required
from nuri.utils.message import created_success, deleted_success, updated_success, error


view = Blueprint("field", __name__)


@view.route("/", methods=["GET"])
@roles_required(Role.ADMIN)
def index():
    fields = Field.query.order_by(Field.collection_id).all()
    return render_template("field/index.html", fields=fields, FieldType=FieldType)


@view.route("/create", methods=["GET", "POST"])
@roles_required(Role.ADMIN)
def create():
    if request.method == "POST":
        name = request.form.get("name")
        alias = request.form.get("alias")
        field_type = request.form.get("field_type")
        collection_id = request.form.get("collection_id")
        is_list = request.form.get("is_list") == "on"
        is_required = request.form.get("is_required") == "on"
        display_field = request.form.get("display_field") == "on"

        excisting_alias = Field.query.filter_by(
            alias=alias, collection_id=collection_id
        ).first()

        if excisting_alias:
            error("Alias already exists")
            return redirect(url_for("field.index"))

        if name and alias:
            new_collection = Field(
                name=name,
                alias=alias,
                collection_id=collection_id,
                field_type=field_type,
                is_list=is_list,
                display_field=display_field,
                is_required=is_required,
            )
            new_collection.save()
            created_success("Field")
            return redirect(url_for("field.index"))

    collections = Collection.query.all()
    return render_template(
        "field/create_or_edit.html", collections=collections, FieldType=FieldType
    )


@view.route("/edit/<int:id>", methods=["GET", "POST"])
@roles_required(Role.ADMIN)
def edit(id):
    field = Field.query.get_or_404(id)

    if request.method == "POST":
        name = request.form.get("name")
        alias = request.form.get("alias")
        field_type = request.form.get("field_type")
        collection_id = request.form.get("collection_id")
        is_list = request.form.get("is_list") == "on"
        is_required = request.form.get("is_required") == "on"
        display_field = request.form.get("display_field") == "on"

        existing_alias = Field.query.filter(
            Field.alias == alias, Field.id != id
        ).first()
        if existing_alias:
            error("Alias already exists")
            return redirect(url_for("field.edit", id=id))

        if name and alias and field_type and collection_id:
            field.name = name
            field.alias = alias
            field.field_type = field_type
            field.is_list = is_list
            field.collection_id = collection_id
            field.is_required = is_required
            field.display_field = display_field
            db.session.commit()
            
            updated_success("Field")
            return redirect(url_for("field.index"))

    collections = Collection.query.all()
    return render_template(
        "field/create_or_edit.html", item=field, collections=collections, FieldType=FieldType
    )


@view.route("/delete/<int:id>", methods=["GET", "POST"])
@roles_required(Role.ADMIN)
def delete(id):
    field = Field.query.get_or_404(id)

    if request.method == "POST":
        field.delete()
        deleted_success("Field")
        return redirect(url_for("field.index"))

    return render_template("field/delete.html", field=field)
