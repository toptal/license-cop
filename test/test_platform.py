import pytest

from test import *
import app.platforms.python
from app.package_version import PackageVersion
from app.github.repository import GithubRepository


@pytest.fixture
def python_platform():
    return app.platforms.python.INSTANCE


@pytest.fixture
def python_repository():
    return GithubRepository('toptal', 'license-cop', http_compression=False)


@pytest.fixture
def ruby_repository():
    return GithubRepository('rails', 'rails', http_compression=False)


@VCR.use_cassette('platform_match_repository.yaml')
def test_match_repository(python_platform, python_repository):
    match = python_platform.match(python_repository)
    assert match is not None
    assert match.platform == python_platform
    assert match.repository == python_repository

    assert len(match.package_descriptors) == 1
    assert match.package_descriptors[0].platform == 'Python'
    assert match.package_descriptors[0].repository == python_repository


@VCR.use_cassette('platform_mismatch_repository.yaml')
def test_mismatch_repository(python_platform, ruby_repository):
    assert python_platform.match(ruby_repository) is None


@VCR.use_cassette('platform_resolve_match.yaml')
def test_resolve_match(python_platform, python_repository):
    match = python_platform.match(python_repository)
    resolutions = match.resolve()

    assert len(resolutions) == 1
    assert resolutions[0].version.id == '{Pipfile}'

    children = resolutions[0].children

    assert children[0].name == 'requests'
    assert children[0].number == '2.18.4'
    assert children[0].is_runtime
    assert children[0].is_tree

    assert children[1].name == 'xmltodict'
    assert children[1].number == '0.11.0'
    assert children[1].is_runtime
    assert children[1].is_leaf

    assert children[2].name == 'pyparsing'
    assert children[2].number == '2.2.0'
    assert children[2].is_runtime
    assert children[2].is_leaf

    assert children[3].name == 'pytest'
    assert children[3].number == '3.2.3'
    assert children[3].is_development
    assert children[3].is_leaf

    assert children[4].name == 'vcrpy'
    assert children[4].number == '1.11.1'
    assert children[4].is_development
    assert children[4].is_leaf

    assert children[5].name == 'pytest-mock'
    assert children[5].number == '1.6.3'
    assert children[5].is_development
    assert children[5].is_tree

    assert children[6].name == 'pep8'
    assert children[6].number == '1.7.0'
    assert children[6].is_development
    assert children[6].is_leaf


@VCR.use_cassette('platform_resolve_match_with_max_depth_of_one.yaml')
def test_resolve_match_with_max_depth_of_one(python_platform, python_repository):
    match = python_platform.match(python_repository)
    resolutions = match.resolve(max_depth=1)

    assert len(resolutions) == 1
    assert resolutions[0].version.id == '{Pipfile}'

    children = resolutions[0].children

    assert children[0].name == 'requests'
    assert children[0].number == '2.18.4'
    assert children[0].is_runtime
    assert children[0].is_leaf

    assert children[1].name == 'xmltodict'
    assert children[1].number == '0.11.0'
    assert children[1].is_runtime
    assert children[1].is_leaf

    assert children[2].name == 'pyparsing'
    assert children[2].number == '2.2.0'
    assert children[2].is_runtime
    assert children[2].is_leaf

    assert children[3].name == 'pytest'
    assert children[3].number == '3.2.3'
    assert children[3].is_development
    assert children[3].is_leaf

    assert children[4].name == 'vcrpy'
    assert children[4].number == '1.11.1'
    assert children[4].is_development
    assert children[4].is_leaf

    assert children[5].name == 'pytest-mock'
    assert children[5].number == '1.6.3'
    assert children[5].is_development
    assert children[5].is_leaf

    assert children[6].name == 'pep8'
    assert children[6].number == '1.7.0'
    assert children[6].is_development
    assert children[6].is_leaf


@VCR.use_cassette('platform_resolve_match_with_max_depth_of_zero.yaml')
def test_resolve_match_with_max_depth_of_zero(python_platform, python_repository):
    match = python_platform.match(python_repository)
    resolutions = match.resolve(max_depth=0)

    assert len(resolutions) == 1
    assert resolutions[0].version.id == '{Pipfile}'
    assert resolutions[0].is_leaf


def test_cache_resolutions_without_max_depth(python_platform, python_repository):
    match = None
    original_resolution = None

    with VCR.use_cassette('platform_resolve_match.yaml'):
        match = python_platform.match(python_repository)
        original_resolution = match.resolve()

    with VCR.use_cassette('no_http_requests.yaml', record_mode='none'):
        assert match.resolve() == original_resolution

    with VCR.use_cassette('platform_resolve_match_with_max_depth_of_one.yaml'):
        assert match.resolve(max_depth=1) != original_resolution


def test_cache_resolutions_with_max_depth(python_platform, python_repository):
    match = None
    original_resolution = None

    with VCR.use_cassette('platform_resolve_match_with_max_depth_of_one.yaml'):
        match = python_platform.match(python_repository)
        original_resolution = match.resolve(max_depth=1)

    with VCR.use_cassette('no_http_requests.yaml', record_mode='none'):
        assert match.resolve(max_depth=1) == original_resolution

    with VCR.use_cassette('platform_resolve_match.yaml'):
        assert match.resolve() != original_resolution
