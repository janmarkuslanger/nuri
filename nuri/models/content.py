from nuri.extensions import db
from .base import BaseModel


class Content(BaseModel):
    __tablename__ = "content"

    collection_id = db.Column(
        db.Integer, db.ForeignKey("collections.id"), nullable=False
    )
    data = db.Column(db.JSON, nullable=False)

    collection = db.relationship("Collection", backref="contents")

    def to_dict(self):
        return {
            "id": self.id,
            "collection_id": self.collection_id,
            "data": self.data,
            "collection": self.collection.to_dict(),
        }
