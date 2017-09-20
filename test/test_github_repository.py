import pytest
import os
from textwrap import dedent

from test import *
from app.github_repository import *


@pytest.fixture
def repository():
    return GithubRepository(
        'toptal',
        'license-cop',
        http_compression=False
    )


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
