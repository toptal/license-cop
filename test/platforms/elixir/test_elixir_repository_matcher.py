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


@VCR.use_cassette('elixir_repository_matcher_mixfile_manifest.yaml')
def test_mixfile_manifest(matcher, elixir_repository):
    match = matcher.match(elixir_repository)

    manifests = match.manifests
    manifest = manifests[0]

    assert manifest.platform == 'Elixir'
    assert manifest.repository == elixir_repository
    assert manifest.paths == ['mix.exs']

    assert manifest.runtime_dependencies == [
        Dependency.runtime('tzdata'),
        Dependency.runtime('combine'),
        Dependency.runtime('gettext')
    ]

    assert manifest.development_dependencies == [
        Dependency.development('ex_doc'),
        Dependency.development('benchfella'),
        Dependency.development('dialyze'),
        Dependency.development('excoveralls')
    ]
