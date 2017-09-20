import os
import pytest


from app.require_environment import *


NAME = 'FOOBAR666'


def reset_environment():
    if NAME in os.environ:
        del(os.environ[NAME])


@pytest.fixture(autouse=True)
def setup(request):
    request.addfinalizer(reset_environment)


def test_environment_variable_is_undefined():
    with pytest.raises(Exception) as e:
        require_environment(NAME)
    assert str(e.value) == 'Required environment value FOOBAR666 is not defined'


def test_environment_variable_is_defined():
    os.environ[NAME] = 'hello world 123!'
    assert require_environment(NAME) == 'hello world 123!'


def test_environment_variable_is_blank():
    os.environ[NAME] = '  '
    with pytest.raises(Exception) as e:
        require_environment(NAME)
    assert str(e.value) == 'Required environment value FOOBAR666 is not defined'
