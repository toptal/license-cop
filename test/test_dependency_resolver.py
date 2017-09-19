import vcr
import pytest

from app.dependency_resolver import *
from app.dependency_resolution import *
from app.package_repository import *
from app.ruby_package_repository import *


@pytest.fixture
def repository(): return RubyPackageRepository(http_compression=False)


@pytest.fixture
def resolver(repository): return DependencyResolver(repository)


@vcr.use_cassette('cassettes/dependency_resolution_without_dependencies.yaml')
def test_resolution_without_dependencies(resolver):
    name = 'rake'
    number = '12.1.0'
    resolution = resolver.resolve_version(DependencyResolutionKind.RUNTIME, name, number)
    resolution.name == name
    assert resolution.is_root
    assert resolution.is_leaf


@vcr.use_cassette('cassettes/dependency_runtime_resolution_without_circular_dependencies.yaml')
def test_runtime_resolution_without_circular_dependencies(resolver):
    root = resolver.resolve_version(DependencyResolutionKind.RUNTIME, 'activesupport', '5.1.4')

    assert len(root.children) == 4

    assert root.children[0].name == 'concurrent-ruby'
    assert root.children[0].is_leaf

    assert root.children[1].name == 'i18n'
    assert root.children[1].is_leaf

    assert root.children[2].name == 'minitest'
    assert root.children[2].is_leaf

    assert root.children[3].name == 'tzinfo'
    assert len(root.children[3].children) == 1
    assert root.children[3].children[0].name == 'thread_safe'
    assert root.children[3].children[0].is_leaf
