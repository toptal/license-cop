import pytest
import requests

from test import *
from app.package_registry import *
from app.platforms.ios.package_registry import *
from app.dependency import *


@pytest.fixture
def registry(): return IosPackageRegistry(http_compression=False)


def test_fetch_version(registry):
    with pytest.raises(RuntimeError) as e:
        registry.fetch_version('Coastline', '2.9.1')
    assert str(e.value) ==\
        'Fetching the specific version for CocoaPods is not supported yet.'


@VCR.use_cassette('ios_package_registry_fetch_latest_version.yaml')
def test_fetch_latest_version(registry):
    version = registry.fetch_latest_version('AWSFacebookSignIn')
    assert version.name == 'AWSFacebookSignIn'
    assert version.number == '2.6.2'
    assert version.licenses == ['Apache License, Version 2.0']
    assert version.development_dependencies == [
    ]
    assert version.runtime_dependencies == [
        Dependency.runtime('AWSAuthCore'),
        Dependency.runtime('FBSDKLoginKit'),
        Dependency.runtime('FBSDKCoreKit')
    ]


@VCR.use_cassette('ios_package_registry_fetch_version_name_not_found.yaml')
def test_fetch_version_name_not_found(registry):
    with pytest.raises(PackageVersionNotFoundError) as e:
        registry.fetch_latest_version('notexists')
    assert str(e.value) ==\
        'Could not find package version notexists:latest. '\
        '404 Client Error: Not Found for url: https://cocoapods.org/pods/notexists'


@VCR.use_cassette('ios_package_registry_fetch_license_from_dict.yaml')
def test_fetch_version_with_license_from_dict(registry):
    version = registry.fetch_latest_version('GoogleMaps')
    assert version.licenses == ['Copyright']


@VCR.use_cassette(
    'ios_package_registry_fetch_version_without_license_but_source_code_uri_has_licensed_github_repository.yaml')
def test_fetch_version_without_license_but_source_code_uri_has_licensed_github_repository(registry):
    version = registry.fetch_latest_version('WebLinking')
    assert version.licenses == ['MIT']
