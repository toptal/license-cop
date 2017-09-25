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
    return DependencyResolution.runtime(build_version(name, number, licenses))


@pytest.fixture
def rails(): return build_version('rails', '5.1.4')


@pytest.fixture
def rake(): return build_version('rake', '12.1.0')


def test_name(rails):
    resolution = DependencyResolution.runtime(rails)
    assert resolution.name == rails.name


def test_number(rails):
    resolution = DependencyResolution.runtime(rails)
    assert resolution.number == rails.number


def test_add_child(rails, rake):
    parent = DependencyResolution.runtime(rails)
    child = DependencyResolution.runtime(rake)

    assert parent.add_child(child) == parent
    assert parent.children == [child]
    assert child.parent == parent


def test_is_root(rails, rake):
    parent = DependencyResolution.runtime(rails)
    child = DependencyResolution.runtime(rake)
    parent.add_child(child)

    assert parent.is_root
    assert not child.is_root


def test_is_leaf(rails, rake):
    parent = DependencyResolution.runtime(rails)
    child = DependencyResolution.runtime(rake)
    parent.add_child(child)

    assert not parent.is_leaf
    assert child.is_leaf


def test_compute_runtime_dependencies(rails):
    resolution = DependencyResolution.runtime(rails)
    dependencies = resolution.dependencies(runtime_only=True)
    assert dependencies == rails.runtime_dependencies


def test_compute_runtime_and_development_dependencies(rails):
    resolution = DependencyResolution.runtime(rails)
    dependencies = resolution.dependencies(runtime_only=False)
    assert dependencies == (rails.runtime_dependencies + rails.development_dependencies)


def test_repr_runtime_dependency_without_children(rails):
    resolution = DependencyResolution.runtime(rails)
    assert repr(resolution) == dedent(
        '''\
        • [runtime] rails:5.1.4 → MIT
        '''
    )


def test_repr_development_dependency_without_children(rails):
    resolution = DependencyResolution.development(rails)
    assert repr(resolution) == dedent(
        '''\
        • [development] rails:5.1.4 → MIT
        '''
    )


def test_repr_dependency_with_unknown_kind_without_children(rails):
    resolution = DependencyResolution(rails, DependencyKind.UNKNOWN)
    assert repr(resolution) == dedent(
        '''\
        • [unknown] rails:5.1.4 → MIT
        '''
    )


def test_repr_with_children(rails):
    resolution = DependencyResolution.development(rails)\
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
        + [development] rails:5.1.4 → MIT
        ⎮--+ [runtime] activesupport:5.1.4 → MIT
        ⎮  ⎮--• [runtime] concurrent-ruby:1.0.2 → BSD
        ⎮  ⎮--• [runtime] i18n:0.7 → Ruby, MIT
        ⎮  ⎮--• [runtime] minitest:5.1 → MIT
        ⎮--+ [runtime] activerecord:5.1.4 → MIT
        ⎮  ⎮--+ [runtime] activemodel:5.1.4 → MIT
        ⎮  ⎮  ⎮--• [runtime] activesupport:5.1.4 → MIT
        ⎮  ⎮--• [runtime] activesupport:5.1.4 → MIT
        ⎮  ⎮--• [runtime] arel:8.0 → Apache
        ⎮--• [runtime] activemodel:5.1.4 → MIT
        '''
    )
