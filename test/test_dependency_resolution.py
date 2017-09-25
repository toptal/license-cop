import pytest
from textwrap import dedent

from app.dependency_resolution import *
from app.package_version import *
from app.dependency import *


def build_version(name, number='5.1.4', licenses=['MIT']):
    return PackageVersion(
        name=name,
        number=number,
        licenses=licenses,
        runtime_dependencies=[
            Dependency.runtime('activesupport'),
            Dependency.runtime('activemodel'),
            Dependency.runtime('activerecord'),
            Dependency.runtime('builder'),
            Dependency.runtime('erubi')
        ],
        development_dependencies=[
            Dependency.development('actionpack'),
            Dependency.development('activemodel')
        ]
    )


def build_resolution(name, number, licenses):
    return DependencyResolution(build_version(name, number, licenses), Dependency.RUNTIME)


@pytest.fixture
def rails(): return build_version('rails', '5.1.4')


@pytest.fixture
def rake(): return build_version('rake', '12.1.0')


def test_name(rails):
    resolution = DependencyResolution(rails, Dependency.RUNTIME)
    assert resolution.name == rails.name


def test_number(rails):
    resolution = DependencyResolution(rails, Dependency.RUNTIME)
    assert resolution.number == rails.number


def test_add_child(rails, rake):
    parent = DependencyResolution(rails, Dependency.RUNTIME)
    child = DependencyResolution(rake, Dependency.RUNTIME)

    assert parent.add_child(child) == parent
    assert parent.children == [child]
    assert child.parent == parent


def test_is_root(rails, rake):
    parent = DependencyResolution(rails, Dependency.RUNTIME)
    child = DependencyResolution(rake, Dependency.RUNTIME)
    parent.add_child(child)

    assert parent.is_root
    assert not child.is_root


def test_is_leaf(rails, rake):
    parent = DependencyResolution(rails, Dependency.RUNTIME)
    child = DependencyResolution(rake, Dependency.RUNTIME)
    parent.add_child(child)

    assert not parent.is_leaf
    assert child.is_leaf


def test_compute_runtime_dependencies(rails):
    resolution = DependencyResolution(rails, Dependency.RUNTIME)
    dependencies = resolution.dependencies(runtime_only=True)
    assert dependencies == rails.runtime_dependencies


def test_compute_runtime_and_development_dependencies(rails):
    resolution = DependencyResolution(rails, Dependency.RUNTIME)
    dependencies = resolution.dependencies(runtime_only=False)
    assert dependencies == (rails.runtime_dependencies + rails.development_dependencies)


def test_repr_without_children(rails):
    resolution = DependencyResolution(rails, Dependency.RUNTIME)
    assert repr(resolution) == dedent(
        '''\
        • rails:5.1.4 → MIT
        '''
    )


def test_repr_with_children(rails):
    resolution = DependencyResolution(rails, Dependency.RUNTIME)\
        .add_child(
            build_resolution('activesupport', '5.1.4', ['MIT'])
                .add_child(build_resolution('concurrent-ruby', '1.0.2', ['BSD']))
                .add_child(build_resolution('i18n', '0.7', ['Ruby', 'MIT']))
                .add_child(build_resolution('minitest', '5.1', ['MIT']))
        )\
        .add_child(
            build_resolution('activerecord', '5.1.4', ['MIT'])
                .add_child(
                    build_resolution('activemodel', '5.1.4', ['MIT'])
                        .add_child(build_resolution('activesupport', '5.1.4', ['MIT']))
                )
                .add_child(build_resolution('activesupport', '5.1.4', ['MIT']))
                .add_child(build_resolution('arel', '8.0', ['Apache']))
        )\
        .add_child(build_resolution('activemodel', '5.1.4', ['MIT']))

    assert repr(resolution) == dedent(
        '''\
        + rails:5.1.4 → MIT
        ⎮--+ activesupport:5.1.4 → MIT
        ⎮  ⎮--• concurrent-ruby:1.0.2 → BSD
        ⎮  ⎮--• i18n:0.7 → Ruby, MIT
        ⎮  ⎮--• minitest:5.1 → MIT
        ⎮--+ activerecord:5.1.4 → MIT
        ⎮  ⎮--+ activemodel:5.1.4 → MIT
        ⎮  ⎮  ⎮--• activesupport:5.1.4 → MIT
        ⎮  ⎮--• activesupport:5.1.4 → MIT
        ⎮  ⎮--• arel:8.0 → Apache
        ⎮--• activemodel:5.1.4 → MIT
        '''
    )
