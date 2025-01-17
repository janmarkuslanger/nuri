from flask import Blueprint, jsonify, request
from app.models import Content, Collection, Field, Asset
from .utils import paginate, resolve_content

view = Blueprint("api", __name__)


@view.route("/content")
def content():
    collection_alias = request.args.get("collection.alias")
    id = request.args.get("id")

    query = Content.query

    if id:
        query = query.filter(Content.id == id)

    if collection_alias:
        query = query.filter(Content.collection.has(alias=collection_alias))

    result = paginate(query)

    result["data"] = resolve_content(result["data"])

    return jsonify(result)


@view.route("/collection")
def collection():
    alias = request.args.get("alias")
    id = request.args.get("id")

    query = Collection.query

    if id:
        query = query.filter(Collection.id == id)

    if alias:
        query = query.filter(Collection.alias == alias)

    result = paginate(query)
    return jsonify(result)


@view.route("/field")
def field():
    alias = request.args.get("alias")
    id = request.args.get("id")

    query = Field.query

    if id:
        query = query.filter(Field.id == id)

    if alias:
        query = query.filter(Field.alias == alias)

    result = paginate(query)
    return jsonify(result)


@view.route("/asset")
def asset():
    name = request.args.get("name")
    id = request.args.get("id")

    query = Asset.query

    if id:
        query = query.filter(Asset.id == id)

    if name:
        query = query.filter(Asset.name == name)

    result = paginate(query)
    return jsonify(result)
