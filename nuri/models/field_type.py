import enum


class FieldType(enum.Enum):
    TEXT = "Text"
    NUMBER = "Number"
    BOOLEAN = "Boolean"
    DATE = "Date"
    ASSET = "Asset"
    COLLECTION = "Collection"
    TEXTAREA = "Textarea"
    RICHTEXT = "RichText"
