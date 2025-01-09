from app import db
from .base import BaseModel

class Collection(BaseModel):
    __tablename__ = "collections"

    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(255))
