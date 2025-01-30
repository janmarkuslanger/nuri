from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()


def init_app(app):
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"


@login_manager.user_loader
def load_user(user_id):
    from nuri.models import User

    User.query.get(int(user_id))
