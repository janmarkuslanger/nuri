from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .base import BaseModel
from .role import Role
from nuri.extensions import db


class User(BaseModel, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    role = db.Column(db.Enum(Role), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password, method="pbkdf2:sha256")

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def has_role(self, role):
        if isinstance(role, Role):
            return self.role == role
        if isinstance(role, str):
            return self.role.value == role
        return False

    def __repr__(self):
        return f"<User {self.email} - {self.role}>"
