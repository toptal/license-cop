import pytest

from test import *
from app.dependency_resolver import *
from app.dependency_resolution import *
from app.platforms.ruby.package_registry import *
from app.platforms.python.package_registry import *


@pytest.fixture
def ruby_resolver():
    return DependencyResolver(RubyPackageRegistry(http_compression=False))


@pytest.fixture
def python_resolver():
    return DependencyResolver(PythonPackageRegistry(http_compression=False))


def check_leaf_status(node, should_be_leaf):
    assert (node.is_leaf == should_be_leaf), (
        f'Node {str(node.version)} has leaf status {node.is_leaf}, but expetation is {should_be_leaf}')


def check_hidden_status(node, should_be_hidden):
    assert (node.hidden == should_be_hidden), (
        f'Node {str(node.version)} has hidden status {node.hidden}, but expetation is {should_be_hidden}')


def check_number(node, expected_number):
    assert node.number == expected_number, (
        f'Node {str(node.version)} does not match version number {expected_number}')


def check_kind(node, expected_kind):
    assert node.kind == expected_kind, (
        f'Node {str(node.version)} with kind {node.kind} does not expected kind {expected_kind}')


def assert_leaf(root, expected_path, expected_number, expected_kind=DependencyKind.RUNTIME):
    assert_path(root, expected_path, expected_number, True, False, expected_kind)


def assert_tree(root, expected_path, expected_number, expected_kind=DependencyKind.RUNTIME):
    assert_path(root, expected_path, expected_number, False, False, expected_kind)


def assert_hide(root, expected_path, expected_number, expected_kind=DependencyKind.RUNTIME):
    assert_path(root, expected_path, expected_number, True, True, expected_kind)


def assert_path(root, expected_path, expected_number, should_be_leaf, should_be_hidden, expected_kind):
    node = root
    for name in expected_path:
        child = next((i for i in node.children if i.name == name), None)
        assert child, f"Path {'→'.join(expected_path)} does not contain {name}"
        node = child

    check_leaf_status(node, should_be_leaf)
    check_hidden_status(node, should_be_hidden)
    check_number(node, expected_number)
    check_kind(node, expected_kind)


def assert_node_match_dependency(node, dependency):
    node.name == dependency.name
    node.kind == dependency.kind


@VCR.use_cassette('dependency_resolution_without_dependencies.yaml')
def test_resolution_without_dependencies(ruby_resolver):
    dependency = Dependency.runtime('rake', '12.1.0')

    root = ruby_resolver.resolve(dependency, runtime_only=True)
    assert_node_match_dependency(root, dependency)
    assert root.is_leaf


@VCR.use_cassette('dependency_runtime_resolution_without_circular_dependencies.yaml')
def test_runtime_resolution_without_circular_dependencies(ruby_resolver):
    dependency = Dependency.runtime('activesupport', '5.1.4')
    root = ruby_resolver.resolve(dependency, runtime_only=True)

    assert_node_match_dependency(root, dependency)
    assert len(root.children) == 4

    assert_leaf(root, ['concurrent-ruby'], '1.0.5')
    assert_leaf(root, ['i18n'], '0.8.6')
    assert_leaf(root, ['minitest'], '5.10.3')
    assert_tree(root, ['tzinfo'], '1.2.3')
    assert_leaf(root, ['tzinfo', 'thread_safe'], '0.3.6')


@VCR.use_cassette('dependency_runtime_resolution_with_circular_dependencies.yaml')
def test_runtime_resolution_with_circular_dependencies(ruby_resolver):
    dependency = Dependency.runtime('rails', '5.1.4')
    root = ruby_resolver.resolve(dependency, runtime_only=True)

    assert_node_match_dependency(root, dependency)
    assert len(root.children) == 11

    assert_tree(root, ['actioncable'], '5.1.4')
    assert_hide(root, ['actioncable', 'actionpack'], '5.1.4')
    assert_leaf(root, ['actioncable', 'nio4r'], '2.1.0')
    assert_tree(root, ['actioncable', 'websocket-driver'], '0.7.0')
    assert_leaf(root, ['actioncable', 'websocket-driver', 'websocket-extensions'], '0.1.2')
    assert_tree(root, ['actionmailer'], '5.1.4')
    assert_hide(root, ['actionmailer', 'actionpack'], '5.1.4')
    assert_hide(root, ['actionmailer', 'actionview'], '5.1.4')
    assert_hide(root, ['actionmailer', 'activejob'], '5.1.4')
    assert_tree(root, ['actionmailer', 'mail'], '2.6.6')
    assert_tree(root, ['actionmailer', 'mail', 'mime-types'], '3.1')
    assert_leaf(root, ['actionmailer', 'mail', 'mime-types', 'mime-types-data'], '3.2016.0521')
    assert_tree(root, ['actionmailer', 'rails-dom-testing'], '2.0.3')
    assert_hide(root, ['actionmailer', 'rails-dom-testing', 'activesupport'], '5.1.4')
    assert_tree(root, ['actionmailer', 'rails-dom-testing', 'nokogiri'], '1.8.1')
    assert_leaf(root, ['actionmailer', 'rails-dom-testing', 'nokogiri', 'mini_portile2'], '2.3.0')
    assert_tree(root, ['actionpack'], '5.1.4')
    assert_hide(root, ['actionpack', 'actionview'], '5.1.4')
    assert_hide(root, ['actionpack', 'activesupport'], '5.1.4')
    assert_leaf(root, ['actionpack', 'rack'], '2.0.3')
    assert_tree(root, ['actionpack', 'rack-test'], '0.7.0')
    assert_leaf(root, ['actionpack', 'rack-test', 'rack'], '2.0.3')
    assert_hide(root, ['actionpack', 'rails-dom-testing'], '2.0.3')
    assert_tree(root, ['actionpack', 'rails-html-sanitizer'], '1.0.3')
    assert_tree(root, ['actionpack', 'rails-html-sanitizer', 'loofah'], '2.1.0')
    assert_hide(root, ['actionpack', 'rails-html-sanitizer', 'loofah', 'nokogiri'], '1.8.1')
    assert_tree(root, ['actionview'], '5.1.4')
    assert_hide(root, ['actionview', 'activesupport'], '5.1.4')
    assert_leaf(root, ['actionview', 'builder'], '3.2.3')
    assert_leaf(root, ['actionview', 'erubi'], '1.6.1')
    assert_hide(root, ['actionview', 'rails-dom-testing'], '2.0.3')
    assert_hide(root, ['actionview', 'rails-html-sanitizer'], '1.0.3')
    assert_hide(root, ['activejob', 'activesupport'], '5.1.4')
    assert_tree(root, ['activejob', 'globalid'], '0.4.0')
    assert_hide(root, ['activejob', 'globalid', 'activesupport'], '5.1.4')
    assert_tree(root, ['activemodel'], '5.1.4')
    assert_hide(root, ['activemodel', 'activesupport'], '5.1.4')
    assert_tree(root, ['activerecord'], '5.1.4')
    assert_hide(root, ['activerecord', 'activemodel'], '5.1.4')
    assert_hide(root, ['activerecord', 'activesupport'], '5.1.4')
    assert_leaf(root, ['activerecord', 'arel'], '8.0.0')
    assert_tree(root, ['activesupport'], '5.1.4')
    assert_leaf(root, ['activesupport', 'concurrent-ruby'], '1.0.5')
    assert_leaf(root, ['activesupport', 'i18n'], '0.8.6')
    assert_leaf(root, ['activesupport', 'minitest'], '5.10.3')
    assert_tree(root, ['activesupport', 'tzinfo'], '1.2.3')
    assert_leaf(root, ['activesupport', 'tzinfo', 'thread_safe'], '0.3.6')
    assert_leaf(root, ['bundler'], '1.15.4')
    assert_tree(root, ['railties'], '5.1.4')
    assert_hide(root, ['railties', 'actionpack'], '5.1.4')
    assert_hide(root, ['railties', 'activesupport'], '5.1.4')
    assert_leaf(root, ['railties', 'method_source'], '0.8.2')
    assert_leaf(root, ['railties', 'rake'], '12.1.0')
    assert_leaf(root, ['railties', 'thor'], '0.20.0')
    assert_tree(root, ['sprockets-rails'], '3.2.1')
    assert_hide(root, ['sprockets-rails', 'actionpack'], '5.1.4')
    assert_hide(root, ['sprockets-rails', 'activesupport'], '5.1.4')
    assert_tree(root, ['sprockets-rails', 'sprockets'], '3.7.1')
    assert_leaf(root, ['sprockets-rails', 'sprockets', 'concurrent-ruby'], '1.0.5')
    assert_leaf(root, ['sprockets-rails', 'sprockets', 'rack'], '2.0.3')


@VCR.use_cassette('dependency_runtime_and_development_resolution_with_circular_dependencies.yaml')
def test_runtime_and_development_resolution_with_circular_dependencies(python_resolver):
    dependency = Dependency.runtime('requests', '2.18.4')
    root = python_resolver.resolve(dependency)

    assert_node_match_dependency(root, dependency)
    assert len(root.children) == 9

    assert_leaf(root, ['win_inet_pton'], '1.0.1', DependencyKind.RUNTIME)
    assert_leaf(root, ['PySocks'], '1.6.7', DependencyKind.RUNTIME)
    assert_tree(root, ['pyOpenSSL'], '17.3.0', DependencyKind.RUNTIME)
    assert_leaf(root, ['pyOpenSSL', 'six'], '1.11.0', DependencyKind.RUNTIME)
    assert_leaf(root, ['pyOpenSSL', 'cryptography'], '2.1.1', DependencyKind.RUNTIME)
    assert_leaf(root, ['pyOpenSSL', 'pytest'], '3.2.3', DependencyKind.DEVELOPMENT)
    assert_leaf(root, ['pyOpenSSL', 'pretend'], '1.0.8', DependencyKind.DEVELOPMENT)
    assert_leaf(root, ['pyOpenSSL', 'flaky'], '3.4.0', DependencyKind.DEVELOPMENT)
    assert_leaf(root, ['pyOpenSSL', 'sphinx_rtd_theme'], '0.2.5b1', DependencyKind.DEVELOPMENT)
    assert_leaf(root, ['pyOpenSSL', 'Sphinx'], '1.6.4', DependencyKind.DEVELOPMENT)
    assert_leaf(root, ['idna'], '2.6', DependencyKind.RUNTIME)
    assert_leaf(root, ['cryptography'], '2.1.1', DependencyKind.RUNTIME)
    assert_tree(root, ['urllib3'], '1.22', DependencyKind.RUNTIME)
    assert_leaf(root, ['urllib3', 'PySocks'], '1.6.7', DependencyKind.RUNTIME)
    assert_leaf(root, ['urllib3', 'ipaddress'], '1.0.18', DependencyKind.RUNTIME)
    assert_leaf(root, ['urllib3', 'certifi'], '2017.7.27.1', DependencyKind.RUNTIME)
    assert_leaf(root, ['urllib3', 'idna'], '2.6', DependencyKind.RUNTIME)
    assert_leaf(root, ['urllib3', 'cryptography'], '2.1.1', DependencyKind.RUNTIME)
    assert_hide(root, ['urllib3', 'pyOpenSSL'], '17.3.0', DependencyKind.RUNTIME)
    assert_leaf(root, ['idna'], '2.6', DependencyKind.RUNTIME)
    assert_leaf(root, ['chardet'], '3.0.4', DependencyKind.RUNTIME)
    assert_leaf(root, ['certifi'], '2017.7.27.1', DependencyKind.RUNTIME)


@VCR.use_cassette('dependency_resolution_with_max_depth_of_one.yaml')
def test_resolution_with_max_depth_of_one(python_resolver):
    dependency = Dependency.runtime('requests', '2.18.4')
    root = python_resolver.resolve(dependency, max_depth=1)

    assert_node_match_dependency(root, dependency)
    assert len(root.children) == 9

    assert_leaf(root, ['win_inet_pton'], '1.0.1', DependencyKind.RUNTIME)
    assert_leaf(root, ['PySocks'], '1.6.7', DependencyKind.RUNTIME)
    assert_leaf(root, ['pyOpenSSL'], '17.3.0', DependencyKind.RUNTIME)
    assert_leaf(root, ['idna'], '2.6', DependencyKind.RUNTIME)
    assert_leaf(root, ['cryptography'], '2.1.1', DependencyKind.RUNTIME)
    assert_leaf(root, ['urllib3'], '1.22', DependencyKind.RUNTIME)
    assert_leaf(root, ['idna'], '2.6', DependencyKind.RUNTIME)
    assert_leaf(root, ['chardet'], '3.0.4', DependencyKind.RUNTIME)
    assert_leaf(root, ['certifi'], '2017.7.27.1', DependencyKind.RUNTIME)


@VCR.use_cassette('dependency_resolution_with_max_depth_of_two.yaml')
def test_resolution_with_max_depth_of_two(python_resolver):
    dependency = Dependency.runtime('requests', '2.18.4')
    root = python_resolver.resolve(dependency, max_depth=2)

    assert_node_match_dependency(root, dependency)
    assert len(root.children) == 9

    assert_leaf(root, ['win_inet_pton'], '1.0.1', DependencyKind.RUNTIME)
    assert_leaf(root, ['PySocks'], '1.6.7', DependencyKind.RUNTIME)
    assert_tree(root, ['pyOpenSSL'], '17.3.0', DependencyKind.RUNTIME)
    assert_leaf(root, ['pyOpenSSL', 'six'], '1.11.0', DependencyKind.RUNTIME)
    assert_leaf(root, ['pyOpenSSL', 'cryptography'], '2.1.1', DependencyKind.RUNTIME)
    assert_leaf(root, ['pyOpenSSL', 'pytest'], '3.2.3', DependencyKind.DEVELOPMENT)
    assert_leaf(root, ['pyOpenSSL', 'pretend'], '1.0.8', DependencyKind.DEVELOPMENT)
    assert_leaf(root, ['pyOpenSSL', 'flaky'], '3.4.0', DependencyKind.DEVELOPMENT)
    assert_leaf(root, ['pyOpenSSL', 'sphinx_rtd_theme'], '0.2.5b1', DependencyKind.DEVELOPMENT)
    assert_leaf(root, ['pyOpenSSL', 'Sphinx'], '1.6.4', DependencyKind.DEVELOPMENT)
    assert_leaf(root, ['idna'], '2.6', DependencyKind.RUNTIME)
    assert_leaf(root, ['cryptography'], '2.1.1', DependencyKind.RUNTIME)
    assert_tree(root, ['urllib3'], '1.22', DependencyKind.RUNTIME)
    assert_leaf(root, ['urllib3', 'PySocks'], '1.6.7', DependencyKind.RUNTIME)
    assert_leaf(root, ['urllib3', 'ipaddress'], '1.0.18', DependencyKind.RUNTIME)
    assert_leaf(root, ['urllib3', 'certifi'], '2017.7.27.1', DependencyKind.RUNTIME)
    assert_leaf(root, ['urllib3', 'idna'], '2.6', DependencyKind.RUNTIME)
    assert_leaf(root, ['urllib3', 'cryptography'], '2.1.1', DependencyKind.RUNTIME)
    assert_hide(root, ['urllib3', 'pyOpenSSL'], '17.3.0', DependencyKind.RUNTIME)
    assert_leaf(root, ['idna'], '2.6', DependencyKind.RUNTIME)
    assert_leaf(root, ['chardet'], '3.0.4', DependencyKind.RUNTIME)
    assert_leaf(root, ['certifi'], '2017.7.27.1', DependencyKind.RUNTIME)


@VCR.use_cassette('dependency_resolution_with_max_depth_of_zero.yaml')
def test_resolution_with_max_depth_of_zero(python_resolver):
    dependency = Dependency.runtime('requests', '2.18.4')
    root = python_resolver.resolve(dependency, max_depth=0)
    assert_node_match_dependency(root, dependency)
    assert root.is_leaf
