import pytest

from test import *
from app.dependency_resolver import *
from app.dependency_resolution import *
from app.platforms.ruby.package_registry import *


@pytest.fixture
def registry(): return RubyPackageRegistry(http_compression=False)


@pytest.fixture
def resolver(registry): return DependencyResolver(registry)


def find_child(node, name):
    for child in node.children:
        if child.name == name:
            return child
    return None


def assert_branch(root, expected_branch, expected_number, is_leaf):
    current_node = root
    for name in expected_branch:
        child = find_child(current_node, name)
        assert child, 'Did not find node with name {0}'.format(name)
        current_node = child

    if is_leaf:
        assert current_node.is_leaf, 'Last node is not leaf, but it is expected to be'
    else:
        assert not current_node.is_leaf, 'Last node is leaf, but it is not expected to be'

    assert current_node.number == expected_number,\
        'Node {0} has number {1} instead of {2}'.format(
            name, current_node.number, expected_number)


@VCR.use_cassette('dependency_resolution_without_dependencies.yaml')
def test_resolution_without_dependencies(resolver):
    dependency = Dependency.runtime('rake', '12.1.0')

    root = resolver.resolve(dependency, runtime_only=True)
    root.name == dependency.name
    root.number == dependency.number
    root.kind == dependency.kind
    assert root.is_root
    assert root.is_leaf


@VCR.use_cassette('dependency_runtime_resolution_without_circular_dependencies.yaml')
def test_runtime_resolution_without_circular_dependencies(resolver):
    dependency = Dependency.runtime('activesupport', '5.1.4')

    root = resolver.resolve(dependency, runtime_only=True)
    root.name == dependency.name
    root.number == dependency.number
    root.kind == dependency.kind
    assert len(root.children) == 4

    assert_branch(root, ['concurrent-ruby'], '1.0.5', True)
    assert_branch(root, ['i18n'], '0.8.6', True)
    assert_branch(root, ['minitest'], '5.10.3', True)
    assert_branch(root, ['tzinfo'], '1.2.3', False)
    assert_branch(root, ['tzinfo', 'thread_safe'], '0.3.6', True)


@VCR.use_cassette('dependency_runtime_resolution_with_circular_dependencies.yaml')
def test_runtime_resolution_with_circular_dependencies(resolver):
    dependency = Dependency.runtime('rails', '5.1.4')

    root = resolver.resolve(dependency, runtime_only=True)
    root.name == dependency.name
    root.number == dependency.number
    root.kind == dependency.kind
    assert len(root.children) == 11

    assert_branch(root, ['actioncable'], '5.1.4', False)
    assert_branch(root, ['actioncable', 'actionpack'], '5.1.4', True)
    assert_branch(root, ['actioncable', 'nio4r'], '2.1.0', True)
    assert_branch(root, ['actioncable', 'websocket-driver'], '0.7.0', False)
    assert_branch(root, ['actioncable', 'websocket-driver', 'websocket-extensions'], '0.1.2', True)

    assert_branch(root, ['actionmailer'], '5.1.4', False)
    assert_branch(root, ['actionmailer', 'actionpack'], '5.1.4', True)
    assert_branch(root, ['actionmailer', 'actionview'], '5.1.4', True)
    assert_branch(root, ['actionmailer', 'activejob'], '5.1.4', True)
    assert_branch(root, ['actionmailer', 'mail'], '2.6.6', False)
    assert_branch(root, ['actionmailer', 'mail', 'mime-types'], '3.1', False)
    assert_branch(root, ['actionmailer', 'mail', 'mime-types', 'mime-types-data'], '3.2016.0521', True)
    assert_branch(root, ['actionmailer', 'rails-dom-testing'], '2.0.3', False)
    assert_branch(root, ['actionmailer', 'rails-dom-testing', 'activesupport'], '5.1.4', True)
    assert_branch(root, ['actionmailer', 'rails-dom-testing', 'nokogiri'], '1.8.1', False)
    assert_branch(root, ['actionmailer', 'rails-dom-testing', 'nokogiri', 'mini_portile2'], '2.3.0', True)

    assert_branch(root, ['actionpack'], '5.1.4', False)
    assert_branch(root, ['actionpack', 'actionview'], '5.1.4', True)
    assert_branch(root, ['actionpack', 'activesupport'], '5.1.4', True)
    assert_branch(root, ['actionpack', 'rack'], '2.0.3', True)
    assert_branch(root, ['actionpack', 'rack-test'], '0.7.0', False)
    assert_branch(root, ['actionpack', 'rack-test', 'rack'], '2.0.3', True)
    assert_branch(root, ['actionpack', 'rails-dom-testing'], '2.0.3', True)
    assert_branch(root, ['actionpack', 'rails-html-sanitizer'], '1.0.3', False)
    assert_branch(root, ['actionpack', 'rails-html-sanitizer', 'loofah'], '2.1.0', False)
    assert_branch(root, ['actionpack', 'rails-html-sanitizer', 'loofah', 'nokogiri'], '1.8.1', True)

    assert_branch(root, ['actionview'], '5.1.4', False)
    assert_branch(root, ['actionview', 'activesupport'], '5.1.4', True)
    assert_branch(root, ['actionview', 'builder'], '3.2.3', True)
    assert_branch(root, ['actionview', 'erubi'], '1.6.1', True)
    assert_branch(root, ['actionview', 'rails-dom-testing'], '2.0.3', True)
    assert_branch(root, ['actionview', 'rails-html-sanitizer'], '1.0.3', True)

    assert_branch(root, ['activejob', 'activesupport'], '5.1.4', True)
    assert_branch(root, ['activejob', 'globalid'], '0.4.0', False)
    assert_branch(root, ['activejob', 'globalid', 'activesupport'], '5.1.4', True)

    assert_branch(root, ['activemodel'], '5.1.4', False)
    assert_branch(root, ['activemodel', 'activesupport'], '5.1.4', True)

    assert_branch(root, ['activerecord'], '5.1.4', False)
    assert_branch(root, ['activerecord', 'activemodel'], '5.1.4', True)
    assert_branch(root, ['activerecord', 'activesupport'], '5.1.4', True)
    assert_branch(root, ['activerecord', 'arel'], '8.0.0', True)

    assert_branch(root, ['activesupport'], '5.1.4', False)
    assert_branch(root, ['activesupport', 'concurrent-ruby'], '1.0.5', True)
    assert_branch(root, ['activesupport', 'i18n'], '0.8.6', True)
    assert_branch(root, ['activesupport', 'minitest'], '5.10.3', True)
    assert_branch(root, ['activesupport', 'tzinfo'], '1.2.3', False)
    assert_branch(root, ['activesupport', 'tzinfo', 'thread_safe'], '0.3.6', True)

    assert_branch(root, ['bundler'], '1.15.4', True)

    assert_branch(root, ['railties'], '5.1.4', False)
    assert_branch(root, ['railties', 'actionpack'], '5.1.4', True)
    assert_branch(root, ['railties', 'activesupport'], '5.1.4', True)
    assert_branch(root, ['railties', 'method_source'], '0.8.2', True)
    assert_branch(root, ['railties', 'rake'], '12.1.0', True)
    assert_branch(root, ['railties', 'thor'], '0.20.0', True)

    assert_branch(root, ['sprockets-rails'], '3.2.1', False)
    assert_branch(root, ['sprockets-rails', 'actionpack'], '5.1.4', True)
    assert_branch(root, ['sprockets-rails', 'activesupport'], '5.1.4', True)
    assert_branch(root, ['sprockets-rails', 'sprockets'], '3.7.1', False)
    assert_branch(root, ['sprockets-rails', 'sprockets', 'concurrent-ruby'], '1.0.5', True)
    assert_branch(root, ['sprockets-rails', 'sprockets', 'rack'], '2.0.3', True)
