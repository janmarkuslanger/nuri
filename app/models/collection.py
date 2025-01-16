from app.extensions import db
from .base import BaseModel


class Collection(BaseModel):
    __tablename__ = "collections"

    name = db.Column(db.String(80), nullable=False)
    alias = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(255))
    fields = db.relationship(
        "Field", backref="collection", cascade="all, delete-orphan"
    )
