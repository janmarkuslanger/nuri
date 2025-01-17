from flask import Blueprint, jsonify, request
from app.models import Content, Collection
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
