from nuri.extensions import db
from .base import BaseModel
from .webhook_type import WebhookType


class WebhookItem(BaseModel):
    __tablename__ = "webhook_items"
    webhook_id = db.Column(
        db.Integer, db.ForeignKey("webhooks.id"), nullable=False
    )
    type = db.Column(db.Enum(WebhookType), nullable=False)
    