import pytest
from textwrap import dedent

from app.dependency_resolution import *
from app.package_version import *
from app.dependency import *


def version(name, number='5.1.4', licenses=['MIT']):
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


@pytest.fixture
def rails(): return version('rails', '5.1.4')


@pytest.fixture
def rake(): return version('rake', '12.1.0')


def test_name(rails):
    node = DependencyResolution.runtime(rails)
    assert node.name == rails.name


def test_number(rails):
    node = DependencyResolution.runtime(rails)
    assert node.number == rails.number


def test_add_child(rails, rake):
    parent = DependencyResolution.runtime(rails)
    child = DependencyResolution.runtime(rake)

    assert parent.add_child(child) == parent
    assert parent.children == [child]
    assert child.parent == parent


def test_hide(rails, rake):
    node = DependencyResolution.runtime(rake, is_hidden=False)
    node.hide()
    assert node.is_hidden


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


def test_get_runtime_dependencies(rails):
    node = DependencyResolution.runtime(rails)
    dependencies = node.dependencies(runtime_only=True)
    assert dependencies == rails.runtime_dependencies


def test_has_runtime_dependencies(rails):
    node = DependencyResolution.runtime(rails)
    assert node.has_dependencies(runtime_only=True)


def test_has_not_runtime_dependencies(rails):
    rails.runtime_dependencies = []
    node = DependencyResolution.runtime(rails)
    assert not node.has_dependencies(runtime_only=True)


def test_get_runtime_and_development_dependencies(rails):
    node = DependencyResolution.runtime(rails)
    dependencies = node.dependencies(runtime_only=False)
    assert dependencies == (rails.runtime_dependencies + rails.development_dependencies)


def test_has_runtime_and_development_dependencies_even_without_runtime_dependencies(rails):
    rails.runtime_dependencies = []
    node = DependencyResolution.runtime(rails)
    assert node.has_dependencies(runtime_only=False)


def test_has_runtime_and_development_dependencies_even_without_development_dependencies(rails):
    rails.development_dependencies = []
    node = DependencyResolution.runtime(rails)
    assert node.has_dependencies(runtime_only=False)


def test_has_not_runtime_nor_dependencies_dependencies(rails):
    rails.runtime_dependencies = []
    rails.development_dependencies = []
    node = DependencyResolution.runtime(rails)
    assert not node.has_dependencies(runtime_only=False)


def test_repr_runtime_dependency_without_children(rails):
    node = DependencyResolution.runtime(rails)
    assert repr(node) == dedent(
        '''\
        - [runtime] rails:5.1.4 → MIT
        '''
    )


def test_repr_development_dependency_without_children(rails):
    node = DependencyResolution.development(rails)
    assert repr(node) == dedent(
        '''\
        - [development] rails:5.1.4 → MIT
        '''
    )


def test_repr_dependency_with_unknown_kind_without_children(rails):
    node = DependencyResolution(rails, DependencyKind.UNKNOWN)
    assert repr(node) == dedent(
        '''\
        - [unknown] rails:5.1.4 → MIT
        '''
    )


def test_repr_hidden_dependency_branch(rails):
    node = DependencyResolution.runtime(rails, is_hidden=True)
    assert repr(node) == dedent(
        '''\
        • [runtime] rails:5.1.4 → MIT
        '''
    )


def test_repr_with_children(rails):
    node = DependencyResolution.development(rails)\
        .add_child(
            DependencyResolution.runtime(version('activesupport', '5.1.4', ['MIT']))
            .add_child(DependencyResolution.runtime(version('concurrent-ruby', '1.0.2', ['BSD'])))
            .add_child(DependencyResolution.runtime(version('i18n', '0.7', ['Ruby', 'MIT'])))
            .add_child(DependencyResolution.runtime(version('minitest', '5.1', ['MIT'])))
        )\
        .add_child(
            DependencyResolution.runtime(version('activerecord', '5.1.4', ['MIT']))
            .add_child(
                DependencyResolution.runtime(version('activemodel', '5.1.4', ['MIT']))
                .add_child(DependencyResolution.runtime(version('activesupport', '5.1.4', ['MIT']), is_hidden=True))
            )
            .add_child(DependencyResolution.development(version('activesupport', '5.1.4', ['MIT']), is_hidden=True))
            .add_child(DependencyResolution.development(version('arel', '8.0', ['Apache'])))
        )\
        .add_child(DependencyResolution.runtime(version('activemodel', '5.1.4', ['MIT']), is_hidden=True))

    assert repr(node) == dedent(
        '''\
        + [development] rails:5.1.4 → MIT
        ⎮--+ [runtime] activesupport:5.1.4 → MIT
        ⎮  ⎮--- [runtime] concurrent-ruby:1.0.2 → BSD
        ⎮  ⎮--- [runtime] i18n:0.7 → Ruby, MIT
        ⎮  ⎮--- [runtime] minitest:5.1 → MIT
        ⎮--+ [runtime] activerecord:5.1.4 → MIT
        ⎮  ⎮--+ [runtime] activemodel:5.1.4 → MIT
        ⎮  ⎮  ⎮--• [runtime] activesupport:5.1.4 → MIT
        ⎮  ⎮--• [development] activesupport:5.1.4 → MIT
        ⎮  ⎮--- [development] arel:8.0 → Apache
        ⎮--• [runtime] activemodel:5.1.4 → MIT
        '''
    )


def test_repr_with_children_and_one_indentation_level(rails):
    node = DependencyResolution.development(rails)\
        .add_child(
            DependencyResolution.runtime(version('activerecord', '5.1.4', ['MIT']))
            .add_child(
                DependencyResolution.runtime(version('activemodel', '5.1.4', ['MIT']))
                .add_child(DependencyResolution.runtime(version('activesupport', '5.1.4', ['MIT']), is_hidden=True))
            )
        )

    assert node.__repr__(1) == dedent(
        '''\
        ⎮--+ [development] rails:5.1.4 → MIT
        ⎮  ⎮--+ [runtime] activerecord:5.1.4 → MIT
        ⎮  ⎮  ⎮--+ [runtime] activemodel:5.1.4 → MIT
        ⎮  ⎮  ⎮  ⎮--• [runtime] activesupport:5.1.4 → MIT
        '''
    )
