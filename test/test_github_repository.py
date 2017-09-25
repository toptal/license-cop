import pytest
import os
from textwrap import dedent

from test import *
from app.github_repository import *


def build_repository(owner, name):
    return GithubRepository(owner, name, http_compression=False)


@pytest.fixture
def repository(): return build_repository('toptal', 'license-cop')


def test_parses_valid_github_url_with_https_scheme():
    repo = GithubRepository.from_url('https://github.com/toptal/license-cop')
    assert repo.owner == 'toptal'
    assert repo.name == 'license-cop'


def test_parses_valid_github_url_with_http_scheme():
    repo = GithubRepository.from_url('http://github.com/toptal/license-cop')
    assert repo.owner == 'toptal'
    assert repo.name == 'license-cop'


def test_parses_valid_github_url_with_git_scheme():
    repo = GithubRepository.from_url('git://github.com/toptal/license-cop.git')
    assert repo.owner == 'toptal'
    assert repo.name == 'license-cop'


def test_parses_valid_github_url_with_git_over_https_scheme():
    repo = GithubRepository.from_url('git+https://github.com/toptal/license-cop.git')
    assert repo.owner == 'toptal'
    assert repo.name == 'license-cop'


def test_parses_valid_github_url_with_git_over_http_scheme():
    repo = GithubRepository.from_url('git+http://github.com/toptal/license-cop.git')
    assert repo.owner == 'toptal'
    assert repo.name == 'license-cop'


def test_parses_valid_github_url_with_double_slash_prefix():
    repo = GithubRepository.from_url('//github.com/toptal/license-cop')
    assert repo.owner == 'toptal'
    assert repo.name == 'license-cop'


def test_parses_valid_github_url_without_scheme():
    repo = GithubRepository.from_url('github.com/toptal/license-cop')
    assert repo.owner == 'toptal'
    assert repo.name == 'license-cop'


def test_parses_valid_github_url_with_slash_at_the_end():
    repo = GithubRepository.from_url('https://github.com/toptal/license-cop/')
    assert repo.owner == 'toptal'
    assert repo.name == 'license-cop'


def test_parses_valid_github_url_with_www_prefix_and_scheme():
    repo = GithubRepository.from_url('https://www.github.com/toptal/license-cop/')
    assert repo.owner == 'toptal'
    assert repo.name == 'license-cop'


def test_parses_valid_github_url_with_www_prefix_but_no_scheme():
    repo = GithubRepository.from_url('www.github.com/toptal/license-cop/')
    assert repo.owner == 'toptal'
    assert repo.name == 'license-cop'


def test_parses_valid_github_url_ignoring_extra_path():
    repo = GithubRepository.from_url('https://github.com/toptal/license-cop/tree/master/packages/foobar')
    assert repo.owner == 'toptal'
    assert repo.name == 'license-cop'


def test_parses_valid_github_url_from_issues_url():
    repo = GithubRepository.from_url('https://github.com/toptal/license-cop/issues')
    assert repo.owner == 'toptal'
    assert repo.name == 'license-cop'


def test_parses_valid_github_url_with_fragment():
    repo = GithubRepository.from_url('https://github.com/toptal/license-cop#readme')
    assert repo.owner == 'toptal'
    assert repo.name == 'license-cop'


def test_parses_github_url_ignoring_case():
    repo = GithubRepository.from_url('HTTP://github.com/TOPTAL/License-Cop')
    assert repo.owner == 'toptal'
    assert repo.name == 'license-cop'


def test_returns_none_when_parsing_invalid_github_url():
    repo = GithubRepository.from_url('https://github.com/foobar')
    assert repo is None


def test_returns_none_when_parsing_non_github_url():
    repo = GithubRepository.from_url('https://bitbucket.com/toptal/license-cop')
    assert repo is None


def test_returns_none_when_parsing_invalid_url():
    repo = GithubRepository.from_url('http:///example.com')
    assert repo is None


@VCR.use_cassette('github_repository_check_path_that_exists.yaml')
def test_check_path_that_exists(repository):
    assert repository.path_exists('fixtures/what_does_the_fox_say.txt')


@VCR.use_cassette('github_repository_check_path_that_does_not_exist.yaml')
def test_check_path_that_does_not_exist(repository):
    assert not repository.path_exists('foobar666.java')


@VCR.use_cassette('github_repository_read_text_file.yaml')
def test_read_text_file(repository):
    text = repository.read_text_file('fixtures/what_does_the_fox_say.txt')
    assert text == dedent(
        """\
        Dog goes "woof"
        Cat goes "meow"
        Bird goes "tweet"
        And mouse goes "squeek"
        Cow goes "moo"
        Frog goes "croak"
        And the elephant goes "toot"
        Ducks say "quack"
        And fish go "blub"
        And the seal goes "ow ow ow"

        But there's one sound
        That no one knows
        What does the fox say?
        """
    )


@VCR.use_cassette('github_repository_read_empty_file.yaml')
def test_read_empty_file(repository):
    text = repository.read_text_file('fixtures/empty_file')
    assert text == ''


@VCR.use_cassette('github_repository_read_directory.yaml')
def test_read_directory(repository):
    with pytest.raises(Exception) as e:
        repository.read_text_file('fixtures')
    assert str(e.value) == 'Path "fixtures" is not a file.'


@VCR.use_cassette('github_repository_with_license.yaml')
def test_with_license():
    license = build_repository('ruby', 'rake').license()
    assert license == 'MIT'


@VCR.use_cassette('github_repository_without_license.yaml')
def test_without_license():
    license = build_repository('toptal', 'license-cop-test-fixture').license()
    assert license is None


def test_str():
    url = 'https://github.com/toptal/license-cop'
    repo = GithubRepository.from_url(url)
    assert str(repo) == url
