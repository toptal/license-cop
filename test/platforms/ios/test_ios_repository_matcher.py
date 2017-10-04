import pytest

from test import *
from app.github.repository import *
from app.platforms.ios.repository_matcher import *


@pytest.fixture
def ios_repository():
    return GithubRepository.from_url(
        'https://github.com/lhc70000/iina',
        http_compression=False
    )


@pytest.fixture
def python_repository():
    return GithubRepository('toptal', 'license-cop', http_compression=False)


@pytest.fixture
def matcher():
    return IosRepositoryMatcher()


@VCR.use_cassette('ios_repository_matcher_match_repository_with_podfile.yaml')
def test_match_repository_with_podfile(matcher, ios_repository):
    assert matcher.match(ios_repository) is not None


@VCR.use_cassette('ios_repository_matcher_mismatch_repository_without_podfile.yaml')
def test_mismatch_repository_without_podfile(matcher, python_repository):
    assert matcher.match(python_repository) is None


@VCR.use_cassette('ios_repository_matcher_single_package_descriptor.yaml')
def test_single_package_descriptor(matcher, ios_repository):
    match = matcher.match(ios_repository)

    descriptors = match.package_descriptors()
    assert len(descriptors) == 1
    descriptor = descriptors[0]

    assert descriptor.platform == 'iOS'
    assert descriptor.repository == ios_repository
    assert descriptor.paths == ['Podfile']

    assert descriptor.runtime_dependencies == [
        Dependency.runtime('MASPreferences'),
        Dependency.runtime('Just'),
        Dependency.runtime('AEXML'),
        Dependency.runtime('PromiseKit'),
        Dependency.runtime('GzipSwift'),
        Dependency.runtime('GRMustache.swift'),
        Dependency.runtime('Sparkle')
    ]

    assert descriptor.development_dependencies == []
