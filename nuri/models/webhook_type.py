import enum


class WebhookType(enum.Enum):
    CONTENT_CREATED = "Content created"
    CONTENT_UPDATED = "Content updated"
    CONTENT_DELETED = "Content deleted"
