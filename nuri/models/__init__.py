from nuri.extensions import login_manager
from .base import BaseModel
from .collection import Collection
from .field import Field
from .field_type import FieldType
from .content import Content
from .asset import Asset
from .user import User
from .role import Role
from .access import Access
from .webhook import Webhook
from .webhook_item import WebhookItem
from .webhook_type import WebhookType
from .request_method import RequestMethod


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
