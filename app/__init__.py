import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nuri.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.urandom(24)

    db.init_app(app) 

    from app.views import collection
    app.register_blueprint(collection, url_prefix='/admin/collections')

    from app.views import field
    app.register_blueprint(field, url_prefix='/admin/fields')

    from app.views import home
    app.register_blueprint(home, url_prefix='/')
    
    return app
