import pytest
import requests

from test import *
from app.package_registry import *
from app.platforms.ruby.package_registry import *
from app.dependency import *


@pytest.fixture
def registry(): return RubyPackageRegistry(http_compression=False)


@VCR.use_cassette('ruby_package_registry_fetch_version.yaml')
def test_fetch_version(registry):
    version = registry.fetch_version('actionview', '4.1.0')
    assert version.name == 'actionview'
    assert version.number == '4.1.0'
    assert version.licenses == ['MIT']
    assert version.development_dependencies == [
        Dependency.development('actionpack'),
        Dependency.development('activemodel')
    ]
    assert version.runtime_dependencies == [
        Dependency.runtime('activesupport'),
        Dependency.runtime('builder'),
        Dependency.runtime('erubi'),
        Dependency.runtime('rails-dom-testing'),
        Dependency.runtime('rails-html-sanitizer')
    ]


@VCR.use_cassette('ruby_package_registry_fetch_latest_version.yaml')
def test_fetch_latest_version(registry):
    version = registry.fetch_latest_version('actionview')
    assert version.name == 'actionview'
    assert version.number == '5.1.4'
    assert version.licenses == ['MIT']
    assert version.development_dependencies == [
        Dependency.development('actionpack'),
        Dependency.development('activemodel')
    ]
    assert version.runtime_dependencies == [
        Dependency.runtime('activesupport'),
        Dependency.runtime('builder'),
        Dependency.runtime('erubi'),
        Dependency.runtime('rails-dom-testing'),
        Dependency.runtime('rails-html-sanitizer')
    ]


@VCR.use_cassette('ruby_package_registry_fetch_version_name_not_found.yaml')
def test_fetch_version_name_not_found(registry):
    with pytest.raises(PackageVersionNotFoundError) as e:
        registry.fetch_version('foobar666', '666')
    assert str(e.value) ==\
        'Could not find package version foobar666:666. '\
        '404 Client Error: Not Found for url: https://rubygems.org/api/v1/gems/foobar666.json'


@VCR.use_cassette('ruby_package_registry_fetch_version_number_not_found.yaml')
def test_fetch_version_number_not_found(registry):
    with pytest.raises(PackageVersionNotFoundError) as e:
        registry.fetch_version('rails', '666')
    assert str(e.value) == 'Could not find package version rails:666.'


@VCR.use_cassette('ruby_package_registry_fetch_latest_version_name_not_found.yaml')
def test_fetch_latest_version_name_not_found(registry):
    with pytest.raises(PackageVersionNotFoundError) as e:
        registry.fetch_latest_version('foobar666')
    assert str(e.value) ==\
        'Could not find package version foobar666:latest. '\
        '404 Client Error: Not Found for url: https://rubygems.org/api/v1/gems/foobar666.json'


@VCR.use_cassette('ruby_package_registry_fetch_version_without_license_nor_code_repository.yaml')
def test_fetch_version_without_license_nor_source_code_repository(registry):
    version = registry.fetch_version('coulda', '0.7.1')
    assert version.licenses == []


@VCR.use_cassette(
    'ruby_package_registry_fetch_version_without_license_but_homepage_uri_has_licensed_github_repository.yaml')
def test_fetch_version_without_license_but_homepage_uri_has_licensed_github_repository(registry):
    version = registry.fetch_version('puffing-billy', '0.10.0')
    assert version.licenses == ['MIT']


@VCR.use_cassette(
    'ruby_package_registry_fetch_version_without_license_but_source_code_uri_has_licensed_github_repository.yaml')
def test_fetch_version_without_license_but_source_code_uri_has_licensed_github_repository(registry):
    version = registry.fetch_version('method_source', '0.8.2')
    assert version.licenses == ['MIT']


@VCR.use_cassette(
    'ruby_package_registry_fetch_version_without_license_and_github_repository_not_found.yaml')
def test_fetch_version_without_license_and_github_repository_not_found(registry, capsys):
    version = registry.fetch_version('rspectacular', '0.70.7')
    assert version.licenses == []


@VCR.use_cassette('ruby_package_registry_fetch_version_without_runtime_dependencies.yaml')
def test_fetch_version_without_runtime_dependencies(registry):
    version = registry.fetch_version('bundler', '1.15.4')
    assert version.runtime_dependencies == []
    assert version.development_dependencies == [
        Dependency.development('automatiek'),
        Dependency.development('mustache'),
        Dependency.development('rake'),
        Dependency.development('rdiscount'),
        Dependency.development('ronn'),
        Dependency.development('rspec')
    ]


@VCR.use_cassette('ruby_package_registry_fetch_version_without_development_dependencies.yaml')
def test_fetch_version_without_development_dependencies(registry):
    version = registry.fetch_version('rails', '5.1.4')
    assert version.runtime_dependencies == [
        Dependency.runtime('actioncable'),
        Dependency.runtime('actionmailer'),
        Dependency.runtime('actionpack'),
        Dependency.runtime('actionview'),
        Dependency.runtime('activejob'),
        Dependency.runtime('activemodel'),
        Dependency.runtime('activerecord'),
        Dependency.runtime('activesupport'),
        Dependency.runtime('bundler'),
        Dependency.runtime('railties'),
        Dependency.runtime('sprockets-rails')
    ]
    assert version.development_dependencies == []
