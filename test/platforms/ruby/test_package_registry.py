import pytest
import requests

from test import *
from app.package_registry import *
from app.platforms.ruby.package_registry import *
from app.dependency import *


@pytest.fixture
def registry(): return RubyPackageRegistry(http_compression=False)


@VCR.use_cassette('ruby_package_registry_version.yaml')
def test_fetch_version(registry):
    version = registry.fetch_version('actionview', '4.1.0')
    assert version.name == 'actionview'
    assert version.number == '4.1.0'
    assert version.licenses == ['MIT']
    assert version.development_dependencies == [
        Dependency('actionpack', Dependency.DEVELOPMENT),
        Dependency('activemodel', Dependency.DEVELOPMENT)
    ]
    assert version.runtime_dependencies == [
        Dependency('activesupport', Dependency.RUNTIME),
        Dependency('builder', Dependency.RUNTIME),
        Dependency('erubi', Dependency.RUNTIME),
        Dependency('rails-dom-testing', Dependency.RUNTIME),
        Dependency('rails-html-sanitizer', Dependency.RUNTIME)
    ]


@VCR.use_cassette('ruby_package_registry_latest_version.yaml')
def test_fetch_latest_version(registry):
    version = registry.fetch_latest_version('actionview')
    assert version.name == 'actionview'
    assert version.number == '5.1.4'
    assert version.licenses == ['MIT']
    assert version.development_dependencies == [
        Dependency('actionpack', Dependency.DEVELOPMENT),
        Dependency('activemodel', Dependency.DEVELOPMENT)
    ]
    assert version.runtime_dependencies == [
        Dependency('activesupport', Dependency.RUNTIME),
        Dependency('builder', Dependency.RUNTIME),
        Dependency('erubi', Dependency.RUNTIME),
        Dependency('rails-dom-testing', Dependency.RUNTIME),
        Dependency('rails-html-sanitizer', Dependency.RUNTIME)
    ]


@VCR.use_cassette('ruby_package_version_name_does_not_exist.yaml')
def test_fetch_version_when_name_does_not_exist(registry):
    with pytest.raises(PackageVersionNotFound) as e:
        registry.fetch_version('foobar666', '666')
    assert str(e.value) ==\
        'Could not find package version foobar666:666. '\
        '404 Client Error: Not Found for url: https://rubygems.org/api/v1/gems/foobar666.json'


@VCR.use_cassette('ruby_package_version_number_does_not_exist.yaml')
def test_fetch_version_when_version_does_not_exist(registry):
    with pytest.raises(PackageVersionNotFound) as e:
        registry.fetch_version('rails', '666')
    assert str(e.value) == 'Could not find package version rails:666.'


@VCR.use_cassette('ruby_package_version_name_does_not_exist.yaml')
def test_fetch_latest_version_when_name_does_not_exist(registry):
    with pytest.raises(PackageVersionNotFound) as e:
        registry.fetch_latest_version('foobar666')
    assert str(e.value) ==\
        'Could not find package version foobar666:latest. '\
        '404 Client Error: Not Found for url: https://rubygems.org/api/v1/gems/foobar666.json'

@VCR.use_cassette('ruby_package_version_without_license_nor_code_repository.yaml')
def test_fetch_version_without_license_nor_source_code_repository(registry):
    version = registry.fetch_version('coulda', '0.7.1')
    assert version.licenses == []


@VCR.use_cassette(
    'ruby_package_version_without_license_but_homepage_uri_has_licensed_github_repository.yaml')
def test_fetch_version_without_license_but_homepage_uri_has_licensed_github_repository(registry):
    version = registry.fetch_version('puffing-billy', '0.10.0')
    assert version.licenses == ['MIT']


@VCR.use_cassette(
    'ruby_package_version_without_license_but_source_code_uri_has_licensed_github_repository.yaml')
def test_fetch_version_without_license_but_source_code_uri_has_licensed_github_repository(registry):
    version = registry.fetch_version('method_source', '0.8.2')
    assert version.licenses == ['MIT']


@VCR.use_cassette('ruby_package_version_without_license_and_github_repository_does_not_exist.yaml')
def test_fetch_version_without_license_and_github_repository_does_not_exist(registry, capsys):
    version = registry.fetch_version('rspectacular', '0.70.7')
    assert version.licenses == []

    _, err = capsys.readouterr()
    assert err == 'WARNING: package specifies invalid GitHub repository '\
                  '[https://github.com/jfelchner/rspectacular]\n'


@VCR.use_cassette('ruby_package_version_without_any_dependencies.yaml')
def test_fetch_version_without_any_dependencies(registry):
    version = registry.fetch_version('rdiscount', '2.2.0.1')
    assert version.runtime_dependencies == []
    assert version.development_dependencies == []


@VCR.use_cassette('ruby_package_version_without_runtime_dependencies.yaml')
def test_fetch_version_without_runtime_dependencies(registry):
    version = registry.fetch_version('bundler', '1.15.4')
    assert version.runtime_dependencies == []
    assert version.development_dependencies == [
        Dependency('automatiek', Dependency.DEVELOPMENT),
        Dependency('mustache', Dependency.DEVELOPMENT),
        Dependency('rake', Dependency.DEVELOPMENT),
        Dependency('rdiscount', Dependency.DEVELOPMENT),
        Dependency('ronn', Dependency.DEVELOPMENT),
        Dependency('rspec', Dependency.DEVELOPMENT)
    ]


@VCR.use_cassette('ruby_package_version_without_development_dependencies.yaml')
def test_fetch_version_without_development_dependencies(registry):
    version = registry.fetch_version('rails', '5.1.4')
    assert version.runtime_dependencies == [
        Dependency('actioncable', Dependency.RUNTIME),
        Dependency('actionmailer', Dependency.RUNTIME),
        Dependency('actionpack', Dependency.RUNTIME),
        Dependency('actionview', Dependency.RUNTIME),
        Dependency('activejob', Dependency.RUNTIME),
        Dependency('activemodel', Dependency.RUNTIME),
        Dependency('activerecord', Dependency.RUNTIME),
        Dependency('activesupport', Dependency.RUNTIME),
        Dependency('bundler', Dependency.RUNTIME),
        Dependency('railties', Dependency.RUNTIME),
        Dependency('sprockets-rails', Dependency.RUNTIME)
    ]
    assert version.development_dependencies == []
