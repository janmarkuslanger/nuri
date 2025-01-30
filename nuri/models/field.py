from nuri.extensions import db
from .base import BaseModel
from .field_type import FieldType


class Field(BaseModel):
    __tablename__ = "fields"

    name = db.Column(db.String(80), nullable=False)
    alias = db.Column(db.String(80), nullable=False)
    field_type = db.Column(db.Enum(FieldType), nullable=False)
    collection_id = db.Column(
        db.Integer, db.ForeignKey("collections.id"), nullable=False
    )
    is_list = db.Column(db.Boolean, default=False, nullable=False)
    is_required = db.Column(db.Boolean, default=False, nullable=False)
    display_field = db.Column(db.Boolean, default=False, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "alias": self.alias,
            "field_type": self.field_type.value,
        }
