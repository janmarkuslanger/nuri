from nuri.extensions import db
from .base import BaseModel


class Access(BaseModel):
    __tablename__ = "access"
    name = db.Column(db.String(80), unique=True, nullable=False)
    api_key = db.Column(db.String(255), unique=True, nullable=True)

    def generate_api_key(self):
        import secrets

        self.api_key = secrets.token_hex(32)
