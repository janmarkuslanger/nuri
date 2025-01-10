from flask import Blueprint
from jinja2 import TemplateNotFound

view = Blueprint('collection', __name__)

@view.route('/')
def list():
    return "Hello World"

@view.route('/<create>')
def create():
    return "Hello World"