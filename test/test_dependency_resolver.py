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


def assert_leaf(root, expected_path, expected_number):
    assert_path(root, expected_path, expected_number, True, False)


def assert_branch(root, expected_path, expected_number):
    assert_path(root, expected_path, expected_number, False, False)


def assert_hidden(root, expected_path, expected_number):
    assert_path(root, expected_path, expected_number, True, True)


def assert_path(root, expected_path, expected_number, leaf, hidden):
    visited_node = root
    for node_name in expected_path:
        child = find_child(visited_node, node_name)
        assert child, 'Path does not contain node with name {0}'.format(node_name)
        visited_node = child

    name = visited_node.name

    if leaf:
        assert visited_node.is_leaf, 'Last node {0} is not leaf, but it is expected to be'.format(name)
    else:
        assert not visited_node.is_leaf, 'Last node {0} is leaf, but it is not expected to be'.format(name)

    if hidden:
        assert visited_node.is_hidden, 'Last node {0} is not hidden, but it is expected to be'.format(name)
    else:
        assert not visited_node.is_hidden, 'Last node {0} is hidden, but it is not expected to be'.format(name)

    assert visited_node.number == expected_number, 'Last node {0} has number {1} instead of {2}'.format(
            name, visited_node.number, expected_number)


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

    assert_leaf(root, ['concurrent-ruby'], '1.0.5')
    assert_leaf(root, ['i18n'], '0.8.6')
    assert_leaf(root, ['minitest'], '5.10.3')
    assert_branch(root, ['tzinfo'], '1.2.3')
    assert_leaf(root, ['tzinfo', 'thread_safe'], '0.3.6')


@VCR.use_cassette('dependency_runtime_resolution_with_circular_dependencies.yaml')
def test_runtime_resolution_with_circular_dependencies(resolver):
    dependency = Dependency.runtime('rails', '5.1.4')

    root = resolver.resolve(dependency, runtime_only=True)
    root.name == dependency.name
    root.number == dependency.number
    root.kind == dependency.kind
    assert len(root.children) == 11

    assert_branch(root, ['actioncable'], '5.1.4')
    assert_hidden(root, ['actioncable', 'actionpack'], '5.1.4')
    assert_leaf(root,   ['actioncable', 'nio4r'], '2.1.0')
    assert_branch(root, ['actioncable', 'websocket-driver'], '0.7.0')
    assert_leaf(root,   ['actioncable', 'websocket-driver', 'websocket-extensions'], '0.1.2')

    assert_branch(root, ['actionmailer'], '5.1.4')
    assert_hidden(root, ['actionmailer', 'actionpack'], '5.1.4')
    assert_hidden(root, ['actionmailer', 'actionview'], '5.1.4')
    assert_hidden(root, ['actionmailer', 'activejob'], '5.1.4')
    assert_branch(root, ['actionmailer', 'mail'], '2.6.6')
    assert_branch(root, ['actionmailer', 'mail', 'mime-types'], '3.1')
    assert_leaf(root,   ['actionmailer', 'mail', 'mime-types', 'mime-types-data'], '3.2016.0521')
    assert_branch(root, ['actionmailer', 'rails-dom-testing'], '2.0.3')
    assert_hidden(root, ['actionmailer', 'rails-dom-testing', 'activesupport'], '5.1.4')
    assert_branch(root, ['actionmailer', 'rails-dom-testing', 'nokogiri'], '1.8.1')
    assert_leaf(root,   ['actionmailer', 'rails-dom-testing', 'nokogiri', 'mini_portile2'], '2.3.0')

    assert_branch(root, ['actionpack'], '5.1.4')
    assert_hidden(root, ['actionpack', 'actionview'], '5.1.4')
    assert_hidden(root, ['actionpack', 'activesupport'], '5.1.4')
    assert_leaf(root,   ['actionpack', 'rack'], '2.0.3')
    assert_branch(root, ['actionpack', 'rack-test'], '0.7.0')
    assert_leaf(root, ['actionpack', 'rack-test', 'rack'], '2.0.3')
    assert_hidden(root, ['actionpack', 'rails-dom-testing'], '2.0.3')
    assert_branch(root, ['actionpack', 'rails-html-sanitizer'], '1.0.3')
    assert_branch(root, ['actionpack', 'rails-html-sanitizer', 'loofah'], '2.1.0')
    assert_hidden(root, ['actionpack', 'rails-html-sanitizer', 'loofah', 'nokogiri'], '1.8.1')

    assert_branch(root, ['actionview'], '5.1.4')
    assert_hidden(root, ['actionview', 'activesupport'], '5.1.4')
    assert_leaf(root,   ['actionview', 'builder'], '3.2.3')
    assert_leaf(root,   ['actionview', 'erubi'], '1.6.1')
    assert_hidden(root, ['actionview', 'rails-dom-testing'], '2.0.3')
    assert_hidden(root, ['actionview', 'rails-html-sanitizer'], '1.0.3')

    assert_hidden(root, ['activejob', 'activesupport'], '5.1.4')
    assert_branch(root, ['activejob', 'globalid'], '0.4.0')
    assert_hidden(root, ['activejob', 'globalid', 'activesupport'], '5.1.4')

    assert_branch(root, ['activemodel'], '5.1.4')
    assert_hidden(root, ['activemodel', 'activesupport'], '5.1.4')

    assert_branch(root, ['activerecord'], '5.1.4')
    assert_hidden(root, ['activerecord', 'activemodel'], '5.1.4')
    assert_hidden(root, ['activerecord', 'activesupport'], '5.1.4')
    assert_leaf(root,   ['activerecord', 'arel'], '8.0.0')

    assert_branch(root, ['activesupport'], '5.1.4')
    assert_leaf(root,   ['activesupport', 'concurrent-ruby'], '1.0.5')
    assert_leaf(root,   ['activesupport', 'i18n'], '0.8.6')
    assert_leaf(root,   ['activesupport', 'minitest'], '5.10.3')
    assert_branch(root, ['activesupport', 'tzinfo'], '1.2.3')
    assert_leaf(root,   ['activesupport', 'tzinfo', 'thread_safe'], '0.3.6')

    assert_leaf(root,   ['bundler'], '1.15.4')

    assert_branch(root, ['railties'], '5.1.4')
    assert_hidden(root, ['railties', 'actionpack'], '5.1.4')
    assert_hidden(root, ['railties', 'activesupport'], '5.1.4')
    assert_leaf(root,   ['railties', 'method_source'], '0.8.2')
    assert_leaf(root,   ['railties', 'rake'], '12.1.0')
    assert_leaf(root,   ['railties', 'thor'], '0.20.0')

    assert_branch(root, ['sprockets-rails'], '3.2.1')
    assert_hidden(root, ['sprockets-rails', 'actionpack'], '5.1.4')
    assert_hidden(root, ['sprockets-rails', 'activesupport'], '5.1.4')
    assert_branch(root, ['sprockets-rails', 'sprockets'], '3.7.1')
    assert_leaf(root,   ['sprockets-rails', 'sprockets', 'concurrent-ruby'], '1.0.5')
    assert_leaf(root, ['sprockets-rails', 'sprockets', 'rack'], '2.0.3')
