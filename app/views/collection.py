from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

view = Blueprint('collection', __name__)

@view.route('/')
def list():
    return "Hello World"