from app.extensions import db
from .base import BaseModel


class Content(BaseModel):
    __tablename__ = "content"

    collection_id = db.Column(
        db.Integer, db.ForeignKey("collections.id"), nullable=False
    )
    data = db.Column(db.JSON, nullable=False)

    collection = db.relationship("Collection", backref="contents")
