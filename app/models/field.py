from app import db
from .base import BaseModel
from .field_type import FieldType

class Field(BaseModel):
    __tablename__ = "fields"

    name = db.Column(db.String(80), nullable=False)
    field_type = db.Column(db.Enum(FieldType), nullable=False)
    collection_id = db.Column(db.Integer, db.ForeignKey("collections.id"), nullable=False)