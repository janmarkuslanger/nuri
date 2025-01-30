from nuri.extensions import db
from .base import BaseModel


class Collection(BaseModel):
    __tablename__ = "collections"

    name = db.Column(db.String(80), nullable=False)
    alias = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(255))
    fields = db.relationship(
        "Field", backref="collection", cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "alias": self.alias,
            "name": self.name,
            "description": self.description,
        }
