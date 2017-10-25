import pytest
import os
from textwrap import dedent

from test import *
from app.github.repository import *


def build_repository(owner, name):
    return GithubRepository(owner, name, http_compression=False)


@pytest.fixture
def repository(): return build_repository('toptal', 'license-cop')


def test_parse_valid_github_url():
    repo = GithubRepository.from_url('https://github.com/acme/foobar')
    assert repo.owner == 'acme'
    assert repo.name == 'foobar'


def test_does_not_parse_invalid_url():
    assert GithubRepository.from_url('https:///foobar') is None


def test_does_not_parse_github_url_without_repository():
    assert GithubRepository.from_url('https://github.com/acme') is None


def test_url(repository):
    assert repository.url == 'https://github.com/toptal/license-cop'


def test_urn(repository):
    assert repository.urn == 'github:toptal:license-cop'


def test_master_url_for_blob_path_with_leading_slash(repository):
    url = repository.master_url('/foo/bar.txt')
    assert url == 'https://github.com/toptal/license-cop/blob/master/foo/bar.txt'


def test_master_url_for_blob_path_without_leading_slash(repository):
    url = repository.master_url('foo/bar.txt')
    assert url == 'https://github.com/toptal/license-cop/blob/master/foo/bar.txt'


def test_master_url_for_tree_path(repository):
    url = repository.master_url('foo/bar.txt', type='tree')
    assert url == 'https://github.com/toptal/license-cop/tree/master/foo/bar.txt'


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
        '''\
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
        '''
    )


@VCR.use_cassette('github_repository_read_empty_file.yaml')
def test_read_empty_file(repository):
    text = repository.read_text_file('fixtures/empty_file')
    assert text == ''


@VCR.use_cassette('github_repository_read_directory.yaml')
def test_read_directory(repository):
    with pytest.raises(ValueError) as e:
        repository.read_text_file('fixtures')
    assert str(e.value) == 'Path "fixtures" is not a file.'


@VCR.use_cassette('github_repository_with_license.yaml')
def test_with_license():
    license = build_repository('ruby', 'rake').license()
    assert license == 'MIT'


@VCR.use_cassette('github_repository_without_license.yaml')
def test_without_license():
    license = build_repository('flavorjones', 'hoe-gemspec').license()
    assert license is None


def test_str():
    url = 'https://github.com/toptal/license-cop'
    repo = GithubRepository.from_url(url)
    assert str(repo) == url


def test_repr():
    url = 'https://github.com/toptal/license-cop'
    repo = GithubRepository.from_url(url)
    assert repr(repo) == 'GitHub repository https://github.com/toptal/license-cop'


def has_blob(tree, path):
    node = tree.navigate(path)
    if node:
        return not node.is_tree


def has_tree(tree, path):
    node = tree.navigate(path)
    if node:
        return node.is_tree


@VCR.use_cassette('github_repository_fetch_master_tree.yaml')
def test_fetch_master_tree():
    repo = GithubRepository.from_url('https://github.com/requests/requests')
    tree = repo.master_tree

    assert has_blob(tree, '.coveragerc')
    assert has_tree(tree, '.github')
    assert has_blob(tree, '.github/ISSUE_TEMPLATE.md')
    assert has_blob(tree, '.gitignore')
    assert has_blob(tree, '.travis.yml')
    assert has_blob(tree, 'AUTHORS.rst')
    assert has_blob(tree, 'CODE_OF_CONDUCT.md')
    assert has_blob(tree, 'CONTRIBUTING.md')
    assert has_blob(tree, 'HISTORY.rst')
    assert has_blob(tree, 'LICENSE')
    assert has_blob(tree, 'MANIFEST.in')
    assert has_blob(tree, 'Makefile')
    assert has_blob(tree, 'Pipfile')
    assert has_blob(tree, 'Pipfile.lock')
    assert has_blob(tree, 'README.rst')
    assert has_tree(tree, '_appveyor')
    assert has_blob(tree, '_appveyor/install.ps1')
    assert has_blob(tree, 'appveyor.yml')
    assert has_tree(tree, 'docs')
    assert has_blob(tree, 'docs/Makefile')
    assert has_tree(tree, 'docs/_static')
    assert has_blob(tree, 'docs/_static/custom.css')
    assert has_blob(tree, 'docs/_static/konami.js')
    assert has_blob(tree, 'docs/_static/requests-logo-small.png')
    assert has_blob(tree, 'docs/_static/requests-sidebar.png')
    assert has_tree(tree, 'docs/_templates')
    assert has_blob(tree, 'docs/_templates/hacks.html')
    assert has_blob(tree, 'docs/_templates/sidebarintro.html')
    assert has_blob(tree, 'docs/_templates/sidebarlogo.html')
    assert has_tree(tree, 'docs/_themes')
    assert has_blob(tree, 'docs/_themes/.gitignore')
    assert has_blob(tree, 'docs/_themes/LICENSE')
    assert has_blob(tree, 'docs/_themes/flask_theme_support.py')
    assert has_blob(tree, 'docs/api.rst')
    assert has_tree(tree, 'docs/community')
    assert has_blob(tree, 'docs/community/faq.rst')
    assert has_blob(tree, 'docs/community/out-there.rst')
    assert has_blob(tree, 'docs/community/recommended.rst')
    assert has_blob(tree, 'docs/community/release-process.rst')
    assert has_blob(tree, 'docs/community/support.rst')
    assert has_blob(tree, 'docs/community/updates.rst')
    assert has_blob(tree, 'docs/community/vulnerabilities.rst')
    assert has_blob(tree, 'docs/conf.py')
    assert has_tree(tree, 'docs/dev')
    assert has_blob(tree, 'docs/dev/authors.rst')
    assert has_blob(tree, 'docs/dev/contributing.rst')
    assert has_blob(tree, 'docs/dev/philosophy.rst')
    assert has_blob(tree, 'docs/dev/todo.rst')
    assert has_blob(tree, 'docs/index.rst')
    assert has_blob(tree, 'docs/make.bat')
    assert has_tree(tree, 'docs/user')
    assert has_blob(tree, 'docs/user/advanced.rst')
    assert has_blob(tree, 'docs/user/authentication.rst')
    assert has_blob(tree, 'docs/user/install.rst')
    assert has_blob(tree, 'docs/user/intro.rst')
    assert has_blob(tree, 'docs/user/quickstart.rst')
    assert has_tree(tree, 'ext')
    assert has_blob(tree, 'ext/requests-logo.ai')
    assert has_blob(tree, 'ext/requests-logo.svg')
    assert has_blob(tree, 'pytest.ini')
    assert has_tree(tree, 'requests')
    assert has_blob(tree, 'requests/__init__.py')
    assert has_blob(tree, 'requests/__version__.py')
    assert has_blob(tree, 'requests/_internal_utils.py')
    assert has_blob(tree, 'requests/adapters.py')
    assert has_blob(tree, 'requests/api.py')
    assert has_blob(tree, 'requests/auth.py')
    assert has_blob(tree, 'requests/certs.py')
    assert has_blob(tree, 'requests/compat.py')
    assert has_blob(tree, 'requests/cookies.py')
    assert has_blob(tree, 'requests/exceptions.py')
    assert has_blob(tree, 'requests/help.py')
    assert has_blob(tree, 'requests/hooks.py')
    assert has_blob(tree, 'requests/models.py')
    assert has_blob(tree, 'requests/packages.py')
    assert has_blob(tree, 'requests/sessions.py')
    assert has_blob(tree, 'requests/status_codes.py')
    assert has_blob(tree, 'requests/structures.py')
    assert has_blob(tree, 'requests/utils.py')
    assert has_blob(tree, 'setup.cfg')
    assert has_blob(tree, 'setup.py')
    assert has_tree(tree, 'tests')
    assert has_blob(tree, 'tests/__init__.py')
    assert has_blob(tree, 'tests/compat.py')
    assert has_blob(tree, 'tests/conftest.py')
    assert has_blob(tree, 'tests/test_help.py')
    assert has_blob(tree, 'tests/test_hooks.py')
    assert has_blob(tree, 'tests/test_lowlevel.py')
    assert has_blob(tree, 'tests/test_packages.py')
    assert has_blob(tree, 'tests/test_requests.py')
    assert has_blob(tree, 'tests/test_structures.py')
    assert has_blob(tree, 'tests/test_testserver.py')
    assert has_blob(tree, 'tests/test_utils.py')
    assert has_tree(tree, 'tests/testserver')
    assert has_blob(tree, 'tests/testserver/__init__.py')
    assert has_blob(tree, 'tests/testserver/server.py')
    assert has_blob(tree, 'tests/utils.py')
    assert has_blob(tree, 'tox.ini')
