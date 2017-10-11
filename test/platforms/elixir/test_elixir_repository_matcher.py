import pytest

from test import *
from app.github.repository import *
from app.platforms.elixir.repository_matcher import *


@pytest.fixture
def elixir_repository():
    return GithubRepository.from_url(
        'https://github.com/bitwalker/timex',
        http_compression=False
    )


@pytest.fixture
def python_repository():
    return GithubRepository('toptal', 'license-cop', http_compression=False)


@pytest.fixture
def matcher():
    return ElixirRepositoryMatcher()


@VCR.use_cassette('elixir_repository_matcher_match_repository_with_mixfile.yaml')
def test_match_repository_with_mixfile(matcher, elixir_repository):
    assert matcher.match(elixir_repository) is not None


@VCR.use_cassette('elixir_repository_matcher_mismatch_repository_without_mixfile.yaml')
def test_mismatch_repository_without_mixfile(matcher, python_repository):
    assert matcher.match(python_repository) is None


@VCR.use_cassette('elixir_repository_matcher_mixfile_package_descriptor.yaml')
def test_mixfile_package_descriptor(matcher, elixir_repository):
    match = matcher.match(elixir_repository)

    descriptors = match.package_descriptors()
    descriptor = descriptors[0]

    assert descriptor.platform == 'Elixir'
    assert descriptor.repository == elixir_repository
    assert descriptor.paths == ['mix.exs']

    assert descriptor.runtime_dependencies == [
        Dependency.runtime('tzdata'),
        Dependency.runtime('combine'),
        Dependency.runtime('gettext')
    ]

    assert descriptor.development_dependencies == [
        Dependency.development('ex_doc'),
        Dependency.development('benchfella'),
        Dependency.development('dialyze'),
        Dependency.development('excoveralls')
    ]
