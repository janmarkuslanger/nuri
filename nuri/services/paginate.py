from flask import request


def generate_paginate(query):
    page = int(request.args.get("page", 1))
    return paginate(query, page)


def paginate(query, page=None, per_page=50):
    if page is None:
        page = 1

    offset = (page - 1) * per_page
    total_items = query.count()
    paginated_data = query.offset(offset).limit(per_page).all()

    serialized_data = [item.to_dict() for item in paginated_data]

    return {
        "data": serialized_data,
        "pagination": {
            "current_page": page,
            "per_page": per_page,
            "total_items": total_items,
        },
    }
