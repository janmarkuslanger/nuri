from sqlalchemy import or_
from nuri.models import Field, FieldType, Content, Asset


def resolve_collection(item):
    collection = item["collection"]
    id = collection["id"]
    data = item["data"]

    resolvable_fields = (
        Field.query.filter(Field.collection_id == id)
        .filter(
            or_(
                Field.field_type == FieldType.COLLECTION,
                Field.field_type == FieldType.ASSET,
            )
        )
        .all()
    )

    resolvable_collection_fields = [
        field for field in resolvable_fields if field.field_type == FieldType.COLLECTION
    ]

    resolvable_asset_fields = [
        field for field in resolvable_fields if field.field_type == FieldType.ASSET
    ]

    asset_ids = []
    for field in resolvable_asset_fields:
        if field.alias not in data:
            continue

        content = data[field.alias]
        ids = content if field.is_list else [content]
        asset_ids.extend(ids)

    asset_items = {
        asset.id: asset.to_dict()
        for asset in Asset.query.filter(Asset.id.in_(asset_ids)).all()
    }

    for field in resolvable_asset_fields:
        data[field.alias] = (
            [asset_items[int(id)] for id in data[field.alias] if field.alias in data]
            if field.is_list
            else asset_items[int(data[field.alias])] if field.alias in data else None
        )

    # TODO: this can be a func
    content_ids = []
    for field in resolvable_collection_fields:
        if field.alias not in data:
            continue

        content = data[field.alias]
        ids = content if field.is_list else [content]
        content_ids.extend(ids)

    content_items = {
        content.id: content.to_dict()
        for content in Content.query.filter(Content.id.in_(content_ids)).all()
    }

    for field in resolvable_collection_fields:
        data[field.alias] = (
            [
                resolve_collection(content_items[int(id)])
                for id in data[field.alias]
                if field.alias in data
            ]
            if field.is_list
            else (
                resolve_collection(content_items[int(data[field.alias])])
                if field.alias in data
                else None
            )
        )

    return item


def resolve_content(data):
    field_cache = {}

    for item in data:
        item = resolve_collection(item)

    return data
