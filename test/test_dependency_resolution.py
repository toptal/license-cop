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


def runtime_node(name, number, licenses, hidden=False):
    return DependencyResolution.runtime(version(name, number, licenses), hidden)


def development_node(name, number, licenses, hidden=False):
    return DependencyResolution.development(version(name, number, licenses), hidden)


@pytest.fixture
def version_not_found():
    return PackageVersionNotFound('foobar')


@pytest.fixture
def rails(): return version('rails', '5.1.4')


@pytest.fixture
def rake(): return version('rake', '12.1.0')


@pytest.fixture
def rails_resolution(rails, version_not_found):
    return (
        DependencyResolution.development(rails)
        .add_child(
            runtime_node('activesupport', '5.1.4', ['MIT'])
            .add_child(runtime_node('concurrent-ruby', '1.0.2', ['BSD']))
            .add_child(runtime_node('i18n', '0.7', ['Ruby', 'MIT']))
            .add_child(development_node('minitest', '5.1', ['MIT']))
        )
        .add_child(DependencyResolution.runtime(version_not_found))
        .add_child(
            runtime_node('activerecord', '5.1.4', ['MIT']).add_child(
                runtime_node('activemodel', '5.1.4', ['MIT']).add_child(
                    runtime_node('activesupport', '5.1.4', ['MIT'], hidden=True))
            )
            .add_child(development_node('activesupport', '5.1.4', ['MIT'], hidden=True))
            .add_child(development_node('arel', '8.0', ['Apache']))
        )
        .add_child(runtime_node('activemodel', '5.1.4', ['MIT'], hidden=True))
    )


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
    node = DependencyResolution.runtime(rake, hidden=False)
    node.hide()
    assert node.hidden


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
        = [runtime] rails:5.1.4 → MIT
        '''
    )


def test_repr_development_dependency_without_children(rails):
    node = DependencyResolution.development(rails)
    assert repr(node) == dedent(
        '''\
        = [development] rails:5.1.4 → MIT
        '''
    )


def test_repr_hidden_dependency_branch(rails):
    node = DependencyResolution.runtime(rails, hidden=True)
    assert repr(node) == dedent(
        '''\
        • [runtime] rails:5.1.4 → MIT
        '''
    )


def test_repr_package_version_not_found(rails):
    version = PackageVersionNotFound('rails')
    node = DependencyResolution.runtime(version)
    assert repr(node) == dedent(
        '''\
        ! [runtime] rails:latest → <version not found on registry>
        '''
    )


def test_repr_with_children(rails_resolution):
    assert repr(rails_resolution) == dedent(
        '''\
        + [development] rails:5.1.4 → MIT
        ⎮--+ [runtime] activesupport:5.1.4 → MIT
        ⎮  ⎮--= [runtime] concurrent-ruby:1.0.2 → BSD
        ⎮  ⎮--= [runtime] i18n:0.7 → Ruby|MIT
        ⎮  ⎮--= [development] minitest:5.1 → MIT
        ⎮--! [runtime] foobar:latest → <version not found on registry>
        ⎮--+ [runtime] activerecord:5.1.4 → MIT
        ⎮  ⎮--+ [runtime] activemodel:5.1.4 → MIT
        ⎮  ⎮  ⎮--• [runtime] activesupport:5.1.4 → MIT
        ⎮  ⎮--• [development] activesupport:5.1.4 → MIT
        ⎮  ⎮--= [development] arel:8.0 → Apache
        ⎮--• [runtime] activemodel:5.1.4 → MIT
        '''
    )


def test_repr_with_children_and_one_indentation_level(rails):
    resolution = (
        DependencyResolution.development(rails)
        .add_child(
            runtime_node('activerecord', '5.1.4', ['MIT'])
            .add_child(
                runtime_node('activemodel', '5.1.4', ['MIT'])
                .add_child(runtime_node('activesupport', '5.1.4', ['MIT'], hidden=True))
            )
        ))

    assert resolution.__repr__(1) == dedent(
        '''\
        ⎮--+ [development] rails:5.1.4 → MIT
        ⎮  ⎮--+ [runtime] activerecord:5.1.4 → MIT
        ⎮  ⎮  ⎮--+ [runtime] activemodel:5.1.4 → MIT
        ⎮  ⎮  ⎮  ⎮--• [runtime] activesupport:5.1.4 → MIT
        '''
    )


def assert_runtime_references(reverse_dependency, name_number_tuples):
    references = reverse_dependency.runtime_references
    assert [(i.name, i.number) for i in references] == name_number_tuples


def assert_development_references(reverse_dependency, name_number_tuples):
    references = reverse_dependency.development_references
    assert [(i.name, i.number) for i in references] == name_number_tuples


def test_reverse_dependencies(rails_resolution):
    r = list(rails_resolution.reverse_dependencies())
    assert len(r) == 8

    assert r[0].name == 'activesupport'
    assert r[0].number == '5.1.4'
    assert_runtime_references(r[0], [
        ('rails', '5.1.4'),
        ('activemodel', '5.1.4')
    ])
    assert_development_references(r[0], [
        ('activerecord', '5.1.4')
    ])

    assert r[1].name == 'concurrent-ruby'
    assert r[1].number == '1.0.2'
    assert_runtime_references(r[1], [('activesupport', '5.1.4')])
    assert_development_references(r[1], [])

    assert r[2].name == 'i18n'
    assert r[2].number == '0.7'
    assert_runtime_references(r[2], [('activesupport', '5.1.4')])
    assert_development_references(r[2], [])

    assert r[3].name == 'minitest'
    assert r[3].number == '5.1'
    assert_runtime_references(r[3], [])
    assert_development_references(r[3], [('activesupport', '5.1.4')])

    assert r[4].name == 'foobar'
    assert r[4].number is None
    assert isinstance(r[4].version, PackageVersionNotFound)
    assert_runtime_references(r[4], [('rails', '5.1.4')])
    assert_development_references(r[4], [])

    assert r[5].name == 'activerecord'
    assert r[5].number == '5.1.4'
    assert_runtime_references(r[5], [('rails', '5.1.4')])
    assert_development_references(r[5], [])

    assert r[6].name == 'activemodel'
    assert r[6].number == '5.1.4'
    assert_runtime_references(r[6], [
        ('activerecord', '5.1.4'),
        ('rails', '5.1.4')
    ])
    assert_development_references(r[6], [])

    assert r[7].name == 'arel'
    assert r[7].number == '8.0'
    assert_runtime_references(r[7], [])
    assert_development_references(r[7], [('activerecord', '5.1.4')])
