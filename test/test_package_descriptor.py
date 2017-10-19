import pytest

from app.github.repository import *
from app.package_descriptor import *
from app.dependency import *


@pytest.fixture
def repository():
    return GithubRepository.from_url('https://github.com/requests/requests')


@pytest.fixture
def platform(): return 'Python'


def test_str_with_one_path(platform, repository):
    d = PackageDescriptor(platform, repository, ['src/app/requirements.txt'], [], [])
    assert str(d) == 'https://github.com/requests/requests {src/app/requirements.txt} [Python]'


def test_str_with_multiple_paths(platform, repository):
    d = PackageDescriptor(platform, repository, ['requirements.txt', 'requirements.test.txt'], [], [])
    assert str(d) == 'https://github.com/requests/requests {requirements.txt|requirements.test.txt} [Python]'


def test_repr(platform, repository):
    d = PackageDescriptor(platform, repository, ['requirements.txt', 'requirements.dev'], [], [])
    assert repr(d) == str(d)


def test_formatted_path_with_one_path(platform, repository):
    d = PackageDescriptor(platform, repository, ['src/app/requirements.txt'], [], [])
    assert d.formatted_paths == 'src/app/requirements.txt'


def test_formatted_path_with_multiple_paths(platform, repository):
    d = PackageDescriptor(platform, repository, ['src/app/requirements.txt', 'src/app/requirements.dev.txt'], [], [])
    assert d.formatted_paths == 'src/app/requirements.txt|src/app/requirements.dev.txt'


def test_urls(platform, repository):
    d = PackageDescriptor(platform, repository, ['src/app/requirements.txt', 'src/app/requirements.dev.txt'], [], [])
    assert d.urls == [
        'https://github.com/requests/requests/blob/master/src/app/requirements.txt',
        'https://github.com/requests/requests/blob/master/src/app/requirements.dev.txt'
    ]


def test_version(platform, repository):
    runtime = [
        Dependency.runtime('activesupport'),
        Dependency.runtime('activemodel'),
        Dependency.runtime('activerecord'),
        Dependency.runtime('builder'),
        Dependency.runtime('erubi')
    ]
    development = [
        Dependency.development('actionpack'),
        Dependency.development('activemodel')
    ]

    d = PackageDescriptor(platform, repository, ['foo', 'bar'], runtime, development)
    assert d.version.name == '{foo|bar}'
    assert d.version.id == '{foo|bar}'
    assert d.version.number is None
    assert d.version.runtime_dependencies == runtime
    assert d.version.development_dependencies == development
