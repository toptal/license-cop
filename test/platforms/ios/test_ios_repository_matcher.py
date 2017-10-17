import pytest

from test import *
from app.github.repository import *
from app.platforms.ios.repository_matcher import *


@pytest.fixture
def podfile_repository():
    return GithubRepository.from_url(
        'https://github.com/lhc70000/iina',
        http_compression=False
    )


@pytest.fixture
def podspec_repository():
    return GithubRepository.from_url(
        'https://github.com/ReactiveX/RxSwift',
        http_compression=False
    )


@pytest.fixture
def python_repository():
    return GithubRepository('toptal', 'license-cop', http_compression=False)


@pytest.fixture
def matcher():
    return IosRepositoryMatcher()


@VCR.use_cassette('ios_repository_matcher_match_repository_with_podfile.yaml')
def test_match_repository_with_podfile(matcher, podfile_repository):
    assert matcher.match(podfile_repository) is not None


@VCR.use_cassette('ios_repository_matcher_mismatch_repository_without_podfile.yaml')
def test_mismatch_repository_without_podfile(matcher, python_repository):
    assert matcher.match(python_repository) is None


@VCR.use_cassette('ios_repository_matcher_extract_from_podfile.yaml')
def test_extract_from_podfile(matcher, podfile_repository):
    match = matcher.match(podfile_repository)

    descriptors = match.package_descriptors()
    assert len(descriptors) == 1
    descriptor = descriptors[0]

    assert descriptor.platform == 'iOS'
    assert descriptor.repository == podfile_repository
    assert descriptor.paths == ['Podfile']

    assert descriptor.runtime_dependencies == set([
        Dependency.runtime('MASPreferences'),
        Dependency.runtime('Just'),
        Dependency.runtime('AEXML'),
        Dependency.runtime('PromiseKit'),
        Dependency.runtime('GzipSwift'),
        Dependency.runtime('GRMustache.swift'),
        Dependency.runtime('Sparkle')
    ])

    assert descriptor.development_dependencies == []


@VCR.use_cassette('ios_repository_matcher_extract_from_podspec.yaml')
def test_extract_from_podspec(matcher, podspec_repository):
    match = matcher.match(podspec_repository)

    descriptors = match.package_descriptors()
    assert len(descriptors) == 1
    descriptor = descriptors[0]

    assert descriptor.platform == 'iOS'
    assert descriptor.repository == podspec_repository
    assert descriptor.paths == ['RxBlocking.podspec', 'RxCocoa.podspec', 'RxSwift.podspec', 'RxTest.podspec']
    print(descriptor.runtime_dependencies)
    assert set(descriptor.runtime_dependencies) == set([
        Dependency.runtime('RxSwift')
    ])

    assert descriptor.development_dependencies == []
