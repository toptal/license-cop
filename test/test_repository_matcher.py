import pytest
from test import *

from app.github.git_node import GitNode
from app.github.repository import GithubRepository
from app.repository_matcher import RepositoryMatcher


class FakeRepositoryMatcher(RepositoryMatcher):
    def __init__(self, patterns):
        super().__init__(patterns)

    def _fetch_manifest(self, repository, match):
        pass


@pytest.fixture
def repository(mocker, tree):
    repo = GithubRepository.from_url('https://github.com/toptal/license-cop')
    mocker.patch.object(repo, 'fetch_tree')
    repo.fetch_tree.return_value = tree
    return repo


@pytest.fixture
def tree():
    root = GitNode.root()
    root.add_blob('requirements.txt')
    root.add_blob('requirements-test.txt')
    root.add_blob('foo/Pipfile')
    root.add_blob('foo/bar/requirements-dev.txt')
    root.add_blob('foo/bar/requirements-docs.txt')
    root.add_blob('foo/bar/foobar.py')
    root.add_blob('foo/bar/Pipfile')
    root.add_blob('foo/bar/beer/Pipfile')
    root.add_blob('Foo.gemspec')
    root.add_blob('Bar.gemspec')
    root.add_blob('README.md')
    root.add_blob('Gemfile')
    root.add_blob('Gemfile.lock')
    root.add_blob('LICENSE')
    return root


def test_one_pattern_mismatch(tree, repository):
    matcher = FakeRepositoryMatcher(['FOOBAR'])
    match = matcher.match(repository)
    assert match is None


def test_multiple_patterns_mismatch(tree, repository):
    matcher = FakeRepositoryMatcher(['FOOBAR', 'hello.py'])
    match = matcher.match(repository)
    assert match is None


def test_one_pattern_match_one_path(tree, repository):
    matcher = FakeRepositoryMatcher(['Gemfile'])
    match = matcher.match(repository)

    assert match is not None
    assert len(match.manifest_matches) == 1
    assert match.manifest_matches[0].nodes == [tree.navigate('Gemfile')]


def test_one_pattern_match_multiple_paths_in_same_directory(tree, repository):
    matcher = FakeRepositoryMatcher(['*.gemspec'])
    match = matcher.match(repository)

    assert match is not None
    assert len(match.manifest_matches) == 1
    assert set(match.manifest_matches[0].nodes) == set([
        tree.navigate('Foo.gemspec'),
        tree.navigate('Bar.gemspec')
    ])


def test_one_pattern_match_multiple_paths_in_multiple_directories(tree, repository):
    matcher = FakeRepositoryMatcher(['Pipfile'])
    match = matcher.match(repository)

    assert match is not None
    assert len(match.manifest_matches) == 3
    assert match.manifest_matches[0].nodes == [tree.navigate('foo/Pipfile')]
    assert match.manifest_matches[1].nodes == [tree.navigate('foo/bar/Pipfile')]
    assert match.manifest_matches[2].nodes == [tree.navigate('foo/bar/beer/Pipfile')]


def test_multiple_patterns_match_multiple_paths_in_multiple_directories(tree, repository):
    matcher = FakeRepositoryMatcher([
        'Pipfile',
        'FOOBAR',
        'requirements*.txt'
    ])
    match = matcher.match(repository)

    assert match is not None
    assert len(match.manifest_matches) == 4
    assert set(match.manifest_matches[0].nodes) == set([
        tree.navigate('requirements.txt'),
        tree.navigate('requirements-test.txt')
    ])
    assert match.manifest_matches[1].nodes == [tree.navigate('foo/Pipfile')]
    assert match.manifest_matches[2].nodes == [
        tree.navigate('foo/bar/Pipfile'),
        tree.navigate('foo/bar/requirements-dev.txt'),
        tree.navigate('foo/bar/requirements-docs.txt')
    ]
    assert match.manifest_matches[3].nodes == [tree.navigate('foo/bar/beer/Pipfile')]
