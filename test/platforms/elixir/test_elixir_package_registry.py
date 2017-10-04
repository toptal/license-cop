import pytest
import requests

from test import *
from app.package_registry import *
from app.platforms.elixir.package_registry import *
from app.dependency import *


@pytest.fixture
def registry(): return ElixirPackageRegistry(http_compression=False)


@VCR.use_cassette('elixir_package_registry_fetch_version.yaml')
def test_fetch_version(registry):
    version = registry.fetch_version('phoenix', '0.2.9')
    assert version.name == 'phoenix'
    assert version.number == '0.2.9'
    assert version.licenses == ['MIT']
    assert version.development_dependencies == []
    assert version.runtime_dependencies == [
        Dependency.runtime('plug'),
        Dependency.runtime('jazz'),
        Dependency.runtime('inflex'),
        Dependency.runtime('ex_conf'),
    ]


@VCR.use_cassette('elixir_package_registry_fetch_latest_version.yaml')
def test_fetch_latest_version(registry):
    version = registry.fetch_latest_version('phoenix')
    assert version.name == 'phoenix'
    assert version.number == '1.3.0'
    assert version.licenses == ['MIT']
    assert version.development_dependencies == [
    ]
    assert version.runtime_dependencies == [
        Dependency.runtime('poison'),
        Dependency.runtime('plug'),
        Dependency.runtime('phoenix_pubsub'),
        Dependency.runtime('cowboy'),
    ]


@VCR.use_cassette('elixir_package_registry_fetch_version_name_not_found.yaml')
def test_fetch_version_name_not_found(registry):
    with pytest.raises(PackageVersionNotFoundError) as e:
        registry.fetch_version('notexists', '0.1.0')
    assert str(e.value) ==\
        'Could not find package version notexists:0.1.0. '\
        '404 Client Error: Not Found for url: https://hex.pm/api/packages/notexists'


@VCR.use_cassette('elixir_package_registry_fetch_version_number_not_found.yaml')
def test_fetch_version_number_not_found(registry):
    with pytest.raises(PackageVersionNotFoundError) as e:
        registry.fetch_version('phoenix', '6.7.1')
    assert str(e.value) ==\
        'Could not find package version phoenix:6.7.1. '\
        '404 Client Error: Not Found for url: https://hex.pm/api/packages/phoenix/releases/6.7.1'


@VCR.use_cassette('elixir_package_registry_fetch_version_without_license_nor_code_repository.yaml')
def test_fetch_version_without_license_nor_source_code_repository(registry):
    version = registry.fetch_version('rat_error', '0.0.1')
    assert version.licenses == []


@VCR.use_cassette(
    'elixir_package_registry_fetch_version_without_license_but_source_code_uri_has_licensed_github_repository.yaml')
def test_fetch_version_without_license_but_source_code_uri_has_licensed_github_repository(registry):
    version = registry.fetch_version('wabbit', '0.3.0')
    assert version.licenses == ['MIT']
