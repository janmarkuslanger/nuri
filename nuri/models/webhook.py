from nuri.extensions import db
from .base import BaseModel
from .request_method import RequestMethod


class Webhook(BaseModel):
    __tablename__ = "webhooks"
    name = db.Column(db.String(80), unique=True, nullable=False)
    request_method = db.Column(db.Enum(RequestMethod), nullable=False, default=RequestMethod.GET)
    url = db.Column(db.String(2048), nullable=False)
    items = db.relationship(
        "WebhookItem", backref="webhook", cascade="all, delete-orphan"
    )