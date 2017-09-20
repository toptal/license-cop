from app.data_object import *


class FixtureObject(DataObject):
    def __init__(self, a_string, a_integer, a_list, a_dict):
        self.a_string = a_string
        self.a_integer = a_integer
        self.a_list = a_list
        self.a_dict = a_dict


def a_object():
    return FixtureObject(
        a_string='foobar',
        a_integer=666,
        a_list=[1, 2, 'three'],
        a_dict={'one': 1, 'two': 2}
    )


def a_slightly_different_object():
    return FixtureObject(
        a_string='foobar',
        a_integer=667,
        a_list=[1, 2, 'three'],
        a_dict={'one': 1, 'two': 2}
    )


def a_very_different_object():
    return FixtureObject(
        a_string='the quick brown fox jumps over the lazy dog',
        a_integer=123,
        a_list=[4],
        a_dict={5: 'five'}
    )


def test_equal_if_objects_are_the_same():
    a = a_object()
    b = a_object()
    assert a == b
    assert not a != b


def test_not_equal_if_objects_are_slightly_different():
    a = a_object()
    b = a_slightly_different_object()
    assert a != b
    assert not a == b


def test_not_equal_if_objects_are_very_different():
    a = a_object()
    b = a_very_different_object()
    assert a != b
    assert not a == b


def test_not_equal_if_objects_are_different_types():
    a = a_object()
    b = 'foobar'
    assert a != b
    assert not a == b


def test_hashes_should_be_the_same_if_objects_are_the_same():
    a = hash(a_object())
    b = hash(a_object())
    assert a == b


def test_hash_should_be_very_different_for_slightly_different_objects():
    a = hash(a_object())
    b = hash(a_slightly_different_object())
    assert a != b
    assert abs(a - b) > 1000000000000000


def test_hash_should_be_very_different_for_very_different_objects():
    a = hash(a_object())
    b = hash(a_very_different_object())
    assert a != b
    assert abs(a - b) > 1000000000000000


def test_str():
    assert str(a_object()) == str({
        'a_string': 'foobar',
        'a_integer': 666,
        'a_list': [1, 2, 'three'],
        'a_dict': {'one': 1, 'two': 2}
    })


def test_repr():
    assert repr(a_object()) == repr({
        'a_string': 'foobar',
        'a_integer': 666,
        'a_list': [1, 2, 'three'],
        'a_dict': {'one': 1, 'two': 2}
    })
