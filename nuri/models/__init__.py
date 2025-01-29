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


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
