import os
from flask import Flask, send_from_directory
from nuri.extensions import init_app
from nuri.extensions import db
from nuri.jinja_utils import getattr_filter


def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///nuri.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.urandom(24)
    app.config["UPLOAD_FOLDER"] = "uploads"

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    init_app(app)

    from nuri.views import (
        collection,
        field,
        content,
        asset,
        home,
        auth,
        user,
        api,
        access,
    )

    app.register_blueprint(collection, url_prefix="/admin/collections")
    app.register_blueprint(field, url_prefix="/admin/fields")
    app.register_blueprint(content, url_prefix="/admin/content")
    app.register_blueprint(asset, url_prefix="/admin/assets")
    app.register_blueprint(user, url_prefix="/admin/user")
    app.register_blueprint(access, url_prefix="/admin/access")
    app.register_blueprint(api, url_prefix="/api")
    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(home, url_prefix="/")

    @app.route("/uploads/<path:filename>")
    def file(filename):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
        return send_from_directory(UPLOAD_FOLDER, filename)

    app.jinja_env.filters["getattr"] = getattr_filter
    
    with app.app_context():
        db.create_all()
        _initialize_admin_user()

    return app

def _initialize_admin_user():
    from nuri.models import User, Role

    if not User.query.filter_by(role=Role.ADMIN).first():
        admin_user = User(
            email="admin@example.com",
            first_name="Admin",
            last_name="User",
            role=Role.ADMIN,
        )
        admin_user.set_password("admin123")
        db.session.add(admin_user)
        db.session.commit()
