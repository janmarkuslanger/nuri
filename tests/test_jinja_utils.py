from nuri.jinja_utils import getattr_filter


class NestedObject:
    name = "Hagebuddne"


class TestObject:
    value = 42
    nested = NestedObject()
    none_nested = None


def test_excisting_simple():
    test_object = TestObject()
    assert getattr_filter(test_object, "value") == 42


def test_none_attribute():
    test_object = TestObject()
    assert getattr_filter(test_object, "my_value") == None


def test_none_object():
    assert getattr_filter(None, "my_value") == None


def test_nested():
    test_object = TestObject()
    assert getattr_filter(test_object, "nested.name") == "Hagebuddne"


def test_none_nested():
    test_object = TestObject()
    assert getattr_filter(test_object, "none_nested.name") == None


def test_nested_none_attribute():
    test_object = TestObject()
    assert getattr_filter(test_object, "nested.a") == None
