import pytest
from test import *

from app.github.repository import *
from app.repository_matcher import *


class FakeRepositoryMatcher(RepositoryMatcher):
    def __init__(self, patterns):
        super().__init__(patterns)

    def _fetch_package_descriptor(self, repository, match):
        pass


@pytest.fixture
def repository(mocker):
    repo = GithubRepository.from_url('https://github.com/toptal/toptal-bot')
    mocker.patch.object(repo, 'path_exists')
    return repo


def test_match_one_pattern_with_one_file(repository):
    repository.path_exists.return_value = True

    pattern = PackageDescriptorPattern.one_file('pipfile', 'Pipfile')
    matcher = FakeRepositoryMatcher([pattern])

    match = matcher.match(repository)
    assert match is not None
    assert len(match.pattern_matches) == 1

    pattern_match = match.pattern_matches[0]
    assert pattern_match.paths == ['Pipfile']
    assert pattern_match.pattern_id == pattern.id


def test_mismatch_one_pattern_with_one_file(repository):
    repository.path_exists.return_value = False

    pattern = PackageDescriptorPattern.one_file('pipfile', 'Pipfile')
    matcher = FakeRepositoryMatcher([pattern])

    assert matcher.match(repository) is None


def test_match_one_pattern_with_multiple_files_where_one_match(repository):
    repository.path_exists.side_effect = [False, True, False]

    pattern = PackageDescriptorPattern.multiple_files('pipfile', ['foo', 'Pipfile', 'bar'])
    matcher = FakeRepositoryMatcher([pattern])

    match = matcher.match(repository)
    assert match is not None
    assert len(match.pattern_matches) == 1

    pattern_match = match.pattern_matches[0]
    assert pattern_match.paths == ['Pipfile']
    assert pattern_match.pattern_id == pattern.id


def test_match_one_pattern_with_multiple_files_where_all_match(repository):
    repository.path_exists.return_value = True

    pattern = PackageDescriptorPattern.multiple_files('pipfile', ['foo', 'Pipfile', 'bar'])
    matcher = FakeRepositoryMatcher([pattern])

    match = matcher.match(repository)
    assert match is not None
    assert len(match.pattern_matches) == 1

    pattern_match = match.pattern_matches[0]
    assert pattern_match.paths == ['foo', 'Pipfile', 'bar']
    assert pattern_match.pattern_id == pattern.id


def test_mismatch_one_pattern_with_multiple_files_where_none_match(repository):
    repository.path_exists.return_value = False

    pattern = PackageDescriptorPattern.multiple_files('pipfile', ['foo', 'Pipfile', 'bar'])
    matcher = FakeRepositoryMatcher([pattern])

    assert matcher.match(repository) is None


def test_match_multiple_patterns_where_one_match(repository):
    repository.path_exists.side_effect = [False, False, False, False, True, False]

    matching_pattern = PackageDescriptorPattern.multiple_files('c', ['package.json', 'foo'])
    matcher = FakeRepositoryMatcher([
        PackageDescriptorPattern.multiple_files('a', ['foo', 'Pipfile', 'bar']),
        PackageDescriptorPattern.one_file('b', 'Gemfile'),
        matching_pattern
    ])

    match = matcher.match(repository)
    assert match is not None

    assert len(match.pattern_matches) == 1
    pattern_match = match.pattern_matches[0]
    assert pattern_match.pattern == matching_pattern
    assert pattern_match.paths == ['package.json']


def test_match_multiple_patterns_where_one_match(repository):
    repository.path_exists.side_effect = [False, False, False, False, True, False]

    matching_pattern = PackageDescriptorPattern.multiple_files('c', ['package.json', 'foo'])
    matcher = FakeRepositoryMatcher([
        PackageDescriptorPattern.multiple_files('a', ['foo', 'Pipfile', 'bar']),
        PackageDescriptorPattern.one_file('b', 'Gemfile'),
        matching_pattern
    ])

    match = matcher.match(repository)
    assert match is not None

    assert len(match.pattern_matches) == 1
    pattern_match = match.pattern_matches[0]
    assert pattern_match.pattern_id == matching_pattern.id
    assert pattern_match.paths == ['package.json']


def test_match_multiple_patterns_where_all_match(repository):
    repository.path_exists.side_effect = [False, True, False, True, True, False]

    patterns = [
        PackageDescriptorPattern.multiple_files('a', ['foo', 'Pipfile', 'bar']),
        PackageDescriptorPattern.one_file('b', 'Gemfile'),
        PackageDescriptorPattern.multiple_files('c', ['package.json', 'foo'])
    ]
    matcher = FakeRepositoryMatcher(patterns)

    match = matcher.match(repository)
    assert match is not None

    assert len(match.pattern_matches) == 3
    assert match.pattern_matches[0].pattern_id == 'a'
    assert match.pattern_matches[0].paths == ['Pipfile']
    assert match.pattern_matches[1].pattern_id == 'b'
    assert match.pattern_matches[1].paths == ['Gemfile']
    assert match.pattern_matches[2].pattern_id == 'c'
    assert match.pattern_matches[2].paths == ['package.json']


def test_mismatch_multiple_patterns(repository):
    repository.path_exists.return_value = False

    patterns = [
        PackageDescriptorPattern.multiple_files('a', ['foo', 'Pipfile', 'bar']),
        PackageDescriptorPattern.one_file('b', 'Gemfile'),
        PackageDescriptorPattern.multiple_files('c', ['package.json', 'foo'])
    ]
    matcher = FakeRepositoryMatcher(patterns)

    assert matcher.match(repository) is None
