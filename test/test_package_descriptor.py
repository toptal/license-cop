import pytest

from app.github_repository import *
from app.package_descriptor import *


@pytest.fixture
def repository():
    return GithubRepository.from_url('https://github.com/rails/rails')


def test_str(repository):
    descriptor = PackageDescriptor('Ruby', repository, 'Gemfile', [], [])
    assert str(descriptor) == 'https://github.com/rails/rails - Ruby [Gemfile]'
