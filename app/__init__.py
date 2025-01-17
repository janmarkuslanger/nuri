import os
from flask import Flask
from app.extensions import init_app

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///nuri.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.urandom(24)
    app.config['UPLOAD_FOLDER'] = 'uploads'

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    init_app(app)

    from app.views import collection, field, content, asset, home, auth, user, api
    app.register_blueprint(collection, url_prefix="/admin/collections")
    app.register_blueprint(field, url_prefix="/admin/fields")
    app.register_blueprint(content, url_prefix="/admin/content")
    app.register_blueprint(asset, url_prefix="/admin/assets")
    app.register_blueprint(user, url_prefix="/admin/user")
    app.register_blueprint(api, url_prefix="/api")
    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(home, url_prefix="/")

    def getattr_filter(obj, attr_name):
        if attr_name is None:
            return False
        return getattr(obj, attr_name, None)

    app.jinja_env.filters["getattr"] = getattr_filter

    return app
