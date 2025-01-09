from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.views import collection

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nuri.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.register_blueprint(collection, url_prefix='/collection')

    db.init_app(app) 
    return app
