from nuri.services.paginate import paginate


def test_paginate_with_default_page(mock_query):
    result = paginate(mock_query)

    assert result["pagination"]["current_page"] == 1
    assert result["pagination"]["per_page"] == 50
    assert result["pagination"]["total_items"] == 100
    assert len(result["data"]) == 50
    assert result["data"][0] == {"id": 1}
