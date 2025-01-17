from app.services.paginate import generate_paginate, paginate
from flask import request

def test_paginate_with_default_page(mock_query):
    result = paginate(mock_query)

    assert result["pagination"]["current_page"] == 1
    assert result["pagination"]["per_page"] == 50
    assert result["pagination"]["total_items"] == 100
    assert len(result["data"]) == 50
    print(result["data"])
    assert result["data"][1] == {"id": 1}
