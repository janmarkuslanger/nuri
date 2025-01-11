from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Field, Collection, FieldType
from app import db

view = Blueprint("field", __name__)


@view.route("/", methods=["GET"])
def index():
    fields = Field.query.all()
    return render_template("field/index.html", fields=fields)

@view.route('/create', methods=["GET", "POST"])
def create():
    if request.method == "POST":
        name = request.form.get("name")
        alias = request.form.get("alias")
        field_type = request.form.get("field_type")
        collection_id = request.form.get("collection_id")
        is_list = request.form.get("is_list") == "on"
        display_field = request.form.get("display_field") == "on"

        excisting_alias = Field.query.filter_by(alias=alias, collection_id=collection_id).first()

        if excisting_alias:
            flash("Alias already exists", "error")
            return redirect(url_for("field.index"))

        if name and alias:
            new_collection = Field(name=name, alias=alias, collection_id=collection_id, field_type=field_type, is_list=is_list, display_field=display_field)
            new_collection.save()
            return redirect(url_for("field.index"))

    collections = Collection.query.all()
    return render_template("field/create.html", collections=collections, FieldType=FieldType)

@view.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    field = Field.query.get_or_404(id)

    if request.method == "POST":
        name = request.form.get("name")
        alias = request.form.get("alias")
        field_type = request.form.get("field_type")
        collection_id = request.form.get("collection_id")
        is_list = request.form.get("is_list") == 'on'
        display_field = request.form.get("display_field") == "on"

        existing_alias = Field.query.filter(Field.alias == alias, Field.id != id).first()
        if existing_alias:
            flash("Alias already exists", "error")
            return redirect(url_for("field.edit", id=id))

        if name and alias and field_type and collection_id:
            field.name = name
            field.alias = alias
            field.field_type = field_type
            field.is_list = is_list
            field.collection_id = collection_id
            field.display_field = display_field
            db.session.commit()
            flash("Field updated successfully!", "success")
            return redirect(url_for("field.index"))
        
    collections = Collection.query.all()
    return render_template("field/edit.html", field=field, collections=collections, FieldType=FieldType)

@view.route("/delete/<int:id>", methods=["GET", "POST"])
def delete(id):
    field = Field.query.get_or_404(id)

    if request.method == "POST":
        field.delete()
        return redirect(url_for("field.index"))

    return render_template("field/delete.html", field=field)
