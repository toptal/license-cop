import pytest
import requests

from test import *
from app.package_registry import *
from app.platforms.nodejs.package_registry import *
from app.dependency import *


@pytest.fixture
def registry(): return NodejsPackageRegistry(http_compression=False)


@VCR.use_cassette('nodejs_package_registry_fetch_version.yaml')
def test_fetch_version(registry):
    version = registry.fetch_version('babel-core', '5.4.3')
    assert version.name == 'babel-core'
    assert version.number == '5.4.3'
    assert version.licenses == ['MIT']
    assert version.development_dependencies == [
        Dependency.development('babel'),
        Dependency.development('browserify'),
        Dependency.development('chai'),
        Dependency.development('eslint'),
        Dependency.development('babel-eslint'),
        Dependency.development('esvalid'),
        Dependency.development('istanbul'),
        Dependency.development('matcha'),
        Dependency.development('mocha'),
        Dependency.development('rimraf'),
        Dependency.development('uglify-js')
    ]
    assert version.runtime_dependencies == [
        Dependency.runtime('acorn-jsx'),
        Dependency.runtime('ast-types'),
        Dependency.runtime('bluebird'),
        Dependency.runtime('chalk'),
        Dependency.runtime('convert-source-map'),
        Dependency.runtime('core-js'),
        Dependency.runtime('debug'),
        Dependency.runtime('detect-indent'),
        Dependency.runtime('esquery'),
        Dependency.runtime('estraverse'),
        Dependency.runtime('esutils'),
        Dependency.runtime('fs-readdir-recursive'),
        Dependency.runtime('globals'),
        Dependency.runtime('is-integer'),
        Dependency.runtime('js-tokens'),
        Dependency.runtime('leven'),
        Dependency.runtime('line-numbers'),
        Dependency.runtime('lodash'),
        Dependency.runtime('minimatch'),
        Dependency.runtime('output-file-sync'),
        Dependency.runtime('path-is-absolute'),
        Dependency.runtime('private'),
        Dependency.runtime('regenerator'),
        Dependency.runtime('regexpu'),
        Dependency.runtime('repeating'),
        Dependency.runtime('resolve'),
        Dependency.runtime('shebang-regex'),
        Dependency.runtime('slash'),
        Dependency.runtime('source-map'),
        Dependency.runtime('source-map-support'),
        Dependency.runtime('strip-json-comments'),
        Dependency.runtime('to-fast-properties'),
        Dependency.runtime('trim-right'),
        Dependency.runtime('user-home')
    ]


@VCR.use_cassette('nodejs_package_registry_fetch_latest_version.yaml')
def test_fetch_latest_version(registry):
    version = registry.fetch_latest_version('babel-core')
    assert version.name == 'babel-core'
    assert version.number == '6.26.0'
    assert version.licenses == ['MIT']
    assert version.development_dependencies == [
        Dependency.development('babel-helper-fixtures'),
        Dependency.development('babel-helper-transform-fixture-test-runner'),
        Dependency.development('babel-polyfill')
    ]
    assert version.runtime_dependencies == [
        Dependency.runtime('babel-code-frame'),
        Dependency.runtime('babel-generator'),
        Dependency.runtime('babel-helpers'),
        Dependency.runtime('babel-messages'),
        Dependency.runtime('babel-register'),
        Dependency.runtime('babel-runtime'),
        Dependency.runtime('babel-template'),
        Dependency.runtime('babel-traverse'),
        Dependency.runtime('babel-types'),
        Dependency.runtime('babylon'),
        Dependency.runtime('convert-source-map'),
        Dependency.runtime('debug'),
        Dependency.runtime('json5'),
        Dependency.runtime('lodash'),
        Dependency.runtime('minimatch'),
        Dependency.runtime('path-is-absolute'),
        Dependency.runtime('private'),
        Dependency.runtime('slash'),
        Dependency.runtime('source-map')
    ]


@VCR.use_cassette('nodejs_package_registry_fetch_version_name_not_found.yaml')
def test_fetch_version_name_not_found(registry):
    with pytest.raises(PackageVersionNotFound) as e:
        registry.fetch_version('foobar666', '4.2.1')
    assert str(e.value) == \
        'Could not find package version foobar666:4.2.1. '\
        '404 Client Error: Not Found for url: http://registry.npmjs.org/foobar666/4.2.1'


@VCR.use_cassette('nodejs_package_registry_fetch_version_number_not_found.yaml')
def test_fetch_version_number_not_found(registry):
    with pytest.raises(PackageVersionNotFound) as e:
        registry.fetch_version('babel-core', '666')
    assert str(e.value) == \
        'Could not find package version babel-core:666. '\
        '404 Client Error: Not Found for url: http://registry.npmjs.org/babel-core/666'


@VCR.use_cassette('nodejs_package_registry_fetch_latest_version_name_not_found.yaml')
def test_fetch_latest_version_name_not_found(registry):
    with pytest.raises(PackageVersionNotFound) as e:
        registry.fetch_latest_version('foobar666')
    assert str(e.value) == \
        'Could not find package version foobar666:latest. '\
        '404 Client Error: Not Found for url: http://registry.npmjs.org/foobar666'


@VCR.use_cassette('nodejs_package_registry_fetch_version_without_license_and_unlicensed_github_repository.yaml')
def test_fetch_version_without_license_and_unlicensed_github_repository(registry):
    version = registry.fetch_version('lodash', '0.3.2')
    assert version.licenses == []


@VCR.use_cassette('nodejs_package_registry_fetch_version_without_license_but_licensed_github_repository.yaml')
def test_fetch_version_without_license(registry):
    version = registry.fetch_version('babel-core', '4.2.1')
    assert version.licenses == ['MIT']


@VCR.use_cassette('nodejs_package_registry_fetch_version_without_development_dependencies.yaml')
def test_fetch_version_without_development_dependencies(registry):
    version = registry.fetch_version('babel-core', '4.2.1')
    assert version.development_dependencies == []


@VCR.use_cassette('nodejs_package_registry_fetch_version_runtime_dependencies.yaml')
def test_fetch_version_without_runtime_dependencies(registry):
    version = registry.fetch_version('lodash', '4.17.4')
    assert version.runtime_dependencies == []
