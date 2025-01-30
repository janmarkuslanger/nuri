import pytest
from flask import Flask
from unittest.mock import MagicMock


@pytest.fixture
def app():
    app = Flask(__name__)
    app.config["TESTING"] = True
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def mock_query():
    mock_query = MagicMock()
    mock_query.count.return_value = 100
    mock_query.offset.return_value.limit.return_value.all.return_value = [
        MagicMock(to_dict=lambda i=i: {"id": i}) for i in range(1, 51)
    ]
    return mock_query
