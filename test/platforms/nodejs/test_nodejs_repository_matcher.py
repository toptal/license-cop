import pytest

from test import *
from app.github.repository import *
from app.platforms.nodejs.repository_matcher import *


@pytest.fixture
def nodejs_repository():
    return GithubRepository.from_url(
        'https://github.com/browserify/browserify',
        http_compression=False
    )


@pytest.fixture
def python_repository():
    return GithubRepository('toptal', 'license-cop', http_compression=False)


@pytest.fixture
def matcher():
    return NodejsRepositoryMatcher()


@VCR.use_cassette('nodejs_repository_matcher_match_repository_with_package_json.yaml')
def test_match_repository_with_package_json(matcher, nodejs_repository):
    assert matcher.match(nodejs_repository) is not None


@VCR.use_cassette('nodejs_repository_matcher_mismatch_repository_without_pacakge_json.yaml')
def test_mismatch_repository_without_pacakge_json(matcher, python_repository):
    assert matcher.match(python_repository) is None


@VCR.use_cassette('nodejs_repository_matcher_package_descriptor.yaml')
def test_package_descriptor(matcher, nodejs_repository):
    match = matcher.match(nodejs_repository)

    descriptors = match.package_descriptors
    descriptor = descriptors[0]

    assert descriptor.platform == 'Node.js'
    assert descriptor.repository == nodejs_repository
    assert descriptor.paths == ['package.json']
    assert descriptor.runtime_dependencies == [
        Dependency.runtime('JSONStream'),
        Dependency.runtime('assert'),
        Dependency.runtime('browser-pack'),
        Dependency.runtime('browser-resolve'),
        Dependency.runtime('browserify-zlib'),
        Dependency.runtime('buffer'),
        Dependency.runtime('cached-path-relative'),
        Dependency.runtime('concat-stream'),
        Dependency.runtime('console-browserify'),
        Dependency.runtime('constants-browserify'),
        Dependency.runtime('crypto-browserify'),
        Dependency.runtime('defined'),
        Dependency.runtime('deps-sort'),
        Dependency.runtime('domain-browser'),
        Dependency.runtime('duplexer2'),
        Dependency.runtime('events'),
        Dependency.runtime('glob'),
        Dependency.runtime('has'),
        Dependency.runtime('htmlescape'),
        Dependency.runtime('https-browserify'),
        Dependency.runtime('inherits'),
        Dependency.runtime('insert-module-globals'),
        Dependency.runtime('labeled-stream-splicer'),
        Dependency.runtime('module-deps'),
        Dependency.runtime('os-browserify'),
        Dependency.runtime('parents'),
        Dependency.runtime('path-browserify'),
        Dependency.runtime('process'),
        Dependency.runtime('punycode'),
        Dependency.runtime('querystring-es3'),
        Dependency.runtime('read-only-stream'),
        Dependency.runtime('readable-stream'),
        Dependency.runtime('resolve'),
        Dependency.runtime('shasum'),
        Dependency.runtime('shell-quote'),
        Dependency.runtime('stream-browserify'),
        Dependency.runtime('stream-http'),
        Dependency.runtime('string_decoder'),
        Dependency.runtime('subarg'),
        Dependency.runtime('syntax-error'),
        Dependency.runtime('through2'),
        Dependency.runtime('timers-browserify'),
        Dependency.runtime('tty-browserify'),
        Dependency.runtime('url'),
        Dependency.runtime('util'),
        Dependency.runtime('vm-browserify'),
        Dependency.runtime('xtend')
    ]

    assert descriptor.development_dependencies == [
        Dependency.development('backbone'),
        Dependency.development('browser-unpack'),
        Dependency.development('coffee-script'),
        Dependency.development('coffeeify'),
        Dependency.development('es6ify'),
        Dependency.development('isstream'),
        Dependency.development('seq'),
        Dependency.development('tap'),
        Dependency.development('temp'),
        Dependency.development('through')
    ]
