from flask import request
from sqlalchemy import or_
from app.models import Field, FieldType, Content, Asset

def paginate(query, page=None, per_page=66):
    if page is None:
        page = int(request.args.get('page', 1))

    offset = (page - 1) * per_page
    total_items = query.count()
    paginated_data = query.offset(offset).limit(per_page).all()
        
    serialized_data = [item.to_dict() for item in paginated_data]

    return {
        'data': serialized_data,
        'pagination': {
            'current_page': page,
            'per_page': per_page,
            'total_items': total_items
        }
    }
    
def resolve_collection(item):
    collection = item["collection"]
    id = collection["id"]
    data = item["data"]
    
    
    resolvable_fields = Field.query.filter(Field.collection_id == id).filter(or_(
        Field.field_type == FieldType.COLLECTION,
        Field.field_type == FieldType.ASSET
    )).all()
    
    resolvable_collection_fields = [
        field 
        for field 
        in resolvable_fields 
        if field.field_type == FieldType.COLLECTION
    ]
    
    resolvable_asset_fields = [
        field 
        for field 
        in resolvable_fields 
        if field.field_type == FieldType.ASSET
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
        for asset 
        in Asset.query.filter(Asset.id.in_(asset_ids)).all()
    }
    
    for field in resolvable_asset_fields:
        data[field.alias] = [asset_items[int(id)] for id in data[field.alias] if field.alias in data]if field.is_list else asset_items[int(data[field.alias])] if field.alias in data else None
    
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
        for content 
        in Content.query.filter(Content.id.in_(content_ids)).all()
    }
    
    for field in resolvable_collection_fields:
        data[field.alias] = (
            [resolve_collection(content_items[int(id)]) 
                for id 
                in data[field.alias] 
                if field.alias in data
            ] if field.is_list else resolve_collection(content_items[int(data[field.alias])]) 
            if field.alias in data else None
        )
    
    return item
    
def resolve_content(data):
    field_cache = {}
    
    for item in data:
        item = resolve_collection(item)
    
    return data
