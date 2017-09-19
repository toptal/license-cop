import pytest

from app.dependency_resolution import *
from app.package_repository import *


def build_version(name, number='5.1.4'):
    return PackageVersion(
        name=name,
        number=number,
        licenses=['MIT'],
        runtime_dependencies=[
            Dependency('activesupport'),
            Dependency('builder'),
            Dependency('erubi'),
            Dependency('rails-dom-testing'),
            Dependency('rails-html-sanitizer')
        ],
        development_dependencies=[
            Dependency('actionpack'),
            Dependency('activemodel')
        ]
    )


def build_runtime_resolution(name):
    version = build_version(name)
    return DependencyResolution(DependencyKind.RUNTIME, version)


@pytest.fixture
def rails(): return build_version('rails', '5.1.4')


@pytest.fixture
def rake(): return build_version('rake', '12.1.0')


def test_scalar_properties(rails):
    resolution = DependencyResolution(DependencyKind.RUNTIME, rails)
    assert resolution.name == rails.name
    assert resolution.number == rails.number
    assert resolution.licenses == rails.licenses


def test_runtime_dependencies(rails):
    resolution = DependencyResolution(DependencyKind.RUNTIME, rails)
    assert resolution.dependencies == rails.runtime_dependencies


def test_development_dependencies(rails):
    resolution = DependencyResolution(DependencyKind.DEVELOPMENT, rails)
    assert resolution.dependencies == rails.development_dependencies


def test_add_child(rails, rake):
    parent = DependencyResolution(DependencyKind.RUNTIME, rails)
    child = DependencyResolution(DependencyKind.RUNTIME, rake)

    parent.add_child(child)
    assert parent.children == [child]
    assert child.parent == parent


def test_is_root(rails, rake):
    parent = DependencyResolution(DependencyKind.RUNTIME, rails)
    child = DependencyResolution(DependencyKind.RUNTIME, rake)
    parent.add_child(child)

    assert parent.is_root
    assert not child.is_root


def test_is_leaf(rails, rake):
    parent = DependencyResolution(DependencyKind.RUNTIME, rails)
    child = DependencyResolution(DependencyKind.RUNTIME, rake)
    parent.add_child(child)

    assert not parent.is_leaf
    assert child.is_leaf
