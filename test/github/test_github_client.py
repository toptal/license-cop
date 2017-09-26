from app.github.client import *


def test_parses_valid_github_url_with_https_scheme():
    parsed = parse_github_url('https://github.com/acme/foobar')
    assert parsed == ('acme', 'foobar', None)


def test_parses_valid_github_url_with_http_scheme():
    parsed = parse_github_url('http://github.com/acme/foobar')
    assert parsed == ('acme', 'foobar', None)


def test_parses_valid_github_url_with_git_scheme():
    parsed = parse_github_url('git://github.com/acme/foobar.git')
    assert parsed == ('acme', 'foobar', None)


def test_parses_valid_github_url_with_git_over_ssh_scheme():
    parsed = parse_github_url('git@github.com:acme/foobar.git')
    assert parsed == ('acme', 'foobar', None)


def test_parses_valid_github_url_with_git_over_https_scheme():
    parsed = parse_github_url('git+https://github.com/acme/foobar.git')
    assert parsed == ('acme', 'foobar', None)


def test_parses_valid_github_url_with_git_over_http_scheme():
    parsed = parse_github_url('git+http://github.com/acme/foobar.git')
    assert parsed == ('acme', 'foobar', None)


def test_parses_valid_github_url_with_double_slash_prefix():
    parsed = parse_github_url('//github.com/acme/foobar')
    assert parsed == ('acme', 'foobar', None)


def test_parses_valid_github_url_without_scheme():
    parsed = parse_github_url('github.com/acme/foobar')
    assert parsed == ('acme', 'foobar', None)


def test_parses_valid_github_url_with_slash_suffix():
    parsed = parse_github_url('https://github.com/acme/foobar/')
    assert parsed == ('acme', 'foobar', None)


def test_parses_valid_github_url_with_www_prefix_and_scheme():
    parsed = parse_github_url('https://www.github.com/acme/foobar/')
    assert parsed == ('acme', 'foobar', None)


def test_parses_valid_github_url_with_www_prefix_but_no_scheme():
    parsed = parse_github_url('www.github.com/acme/foobar')
    assert parsed == ('acme', 'foobar', None)


def test_parses_valid_github_url_without_repository():
    parsed = parse_github_url('https://github.com/acme')
    assert parsed == ('acme', None, None)


def test_parses_valid_github_url_without_repository_with_slash_suffix():
    parsed = parse_github_url('https://github.com/acme/')
    assert parsed == ('acme', None, None)


def test_parses_valid_github_url_with_path():
    parsed = parse_github_url('https://github.com/acme/foobar/tree/master/packages/foobar')
    assert parsed == ('acme', 'foobar', 'tree/master/packages/foobar')


def test_parses_valid_github_url_with_fragment():
    parsed = parse_github_url('https://github.com/acme/foobar#readme')
    assert parsed == ('acme', 'foobar', '#readme')


def test_parses_valid_github_url_with_path_and_fragment():
    parsed = parse_github_url('https://github.com/acme/foobar/tree/master#readme')
    assert parsed == ('acme', 'foobar', 'tree/master#readme')


def test_parses_valid_github_url_with_dots():
    parsed = parse_github_url('https://github.com/acme/foo.bar')
    assert parsed == ('acme', 'foo.bar', None)


def test_parses_valid_github_url_with_underscore():
    parsed = parse_github_url('https://github.com/acme/foo_bar')
    assert parsed == ('acme', 'foo_bar', None)


def test_parses_valid_github_url_with_dashes():
    parsed = parse_github_url('https://github.com/ac-me/foo-bar')
    assert parsed == ('ac-me', 'foo-bar', None)


def test_parses_valid_github_url_with_numbers():
    parsed = parse_github_url('https://github.com/acme123/foobar666')
    assert parsed == ('acme123', 'foobar666', None)


def test_parses_valid_github_url_with_dots_and_git_suffix():
    parsed = parse_github_url('https://github.com/acme/foo.bar.git')
    assert parsed == ('acme', 'foo.bar', None)


def test_parses_valid_github_url_ignoring_case():
    parsed = parse_github_url('HTTP://github.com/ACME/FooBar#README')
    assert parsed == ('acme', 'foobar', '#readme')


def test_returns_none_when_parsing_github_url_without_owner_nor_repository():
    assert parse_github_url('https://github.com/') is None


def test_returns_none_when_parsing_non_github_url():
    assert parse_github_url('https://bitbucket.com/acme/foobar') is None


def test_returns_none_when_parsing_invalid_url():
    assert parse_github_url('http:///example.com') is None
