from flask_sqlalchemy import SQLAlchemy
from nuri.extensions import db
from .base import BaseModel


class Asset(BaseModel):
    __tablename__ = "assets"

    name = db.Column(db.String(255), nullable=False)
    path = db.Column(db.String(255), nullable=False, unique=True)
    is_public = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"<Asset {self.id}: {self.name}, Public: {self.is_public}>"

    def to_dict(self):
        return {"id": self.id, "name": self.name, "path": self.path}
