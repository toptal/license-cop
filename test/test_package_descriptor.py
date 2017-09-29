import pytest

from app.github.repository import *
from app.package_descriptor import *


@pytest.fixture
def repository():
    return GithubRepository.from_url('https://github.com/requests/requests')


def test_str_with_one_path(repository):
    paths = ['src/app/requirements.txt']
    descriptor = PackageDescriptor('Python', repository, paths, [], [])

    assert str(descriptor) == \
        'https://github.com/requests/requests - Python [src/app/requirements.txt]'


def test_str_with_multiple_paths(repository):
    paths = ['requirements.txt', 'requirements.test.txt']
    descriptor = PackageDescriptor('Python', repository, paths, [], [])

    assert str(descriptor) == (
        'https://github.com/requests/requests - Python '
        '[requirements.txt, requirements.test.txt]'
    )
