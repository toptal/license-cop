import vcr
import pytest
import requests

from app.ruby_package_repository import *


@pytest.fixture
def repository(): return RubyPackageRepository(http_compression=False)


@vcr.use_cassette('cassettes/ruby_package_repository_version.yaml')
def test_fetch_version(repository):
    version = repository.fetch_version('actionview', '4.1.0')
    assert version.name == 'actionview'
    assert version.number == '4.1.0'
    assert version.licenses == ['MIT']
    assert version.development_dependencies == [
        Dependency('actionpack'),
        Dependency('activemodel')
    ]
    assert version.runtime_dependencies == [
        Dependency('activesupport'),
        Dependency('builder'),
        Dependency('erubi'),
        Dependency('rails-dom-testing'),
        Dependency('rails-html-sanitizer')
    ]


@vcr.use_cassette('cassettes/ruby_package_repository_latest_version.yaml')
def test_fetch_latest_version(repository):
    version = repository.fetch_latest_version('actionview')
    assert version.name == 'actionview'
    assert version.number == '5.1.4'
    assert version.licenses == ['MIT']
    assert version.development_dependencies == [
        Dependency('actionpack'),
        Dependency('activemodel')
    ]
    assert version.runtime_dependencies == [
        Dependency('activesupport'),
        Dependency('builder'),
        Dependency('erubi'),
        Dependency('rails-dom-testing'),
        Dependency('rails-html-sanitizer')
    ]


@vcr.use_cassette('cassettes/ruby_package_version_name_does_not_exist.yaml')
def test_fetch_version_when_name_does_not_exist(repository):
    with pytest.raises(requests.exceptions.HTTPError):
        repository.fetch_version('foobar666', '666')


@vcr.use_cassette('cassettes/ruby_package_version_number_does_not_exist.yaml')
def test_fetch_version_when_version_does_not_exist(repository):
    with pytest.raises(Exception) as e:
        repository.fetch_version('rails', '666')
    assert str(e.value) == 'Could not find Ruby gem rails:666'


@vcr.use_cassette('cassettes/ruby_package_version_name_does_not_exist.yaml')
def test_fetch_latest_version_when_name_does_not_exist(repository):
    with pytest.raises(requests.exceptions.HTTPError):
        repository.fetch_latest_version('foobar666')


@vcr.use_cassette('cassettes/ruby_package_version_without_license.yaml')
def test_fetch_version_without_license(repository):
    version = repository.fetch_version('coulda', '0.7.1')
    assert version.licenses == []


@vcr.use_cassette('cassettes/ruby_package_version_without_any_dependencies.yaml')
def test_fetch_version_without_any_dependencies(repository):
    version = repository.fetch_version('rdiscount', '2.2.0.1')
    assert version.runtime_dependencies == []
    assert version.development_dependencies == []


@vcr.use_cassette('cassettes/ruby_package_version_without_runtime_dependencies.yaml')
def test_fetch_version_without_runtime_dependencies(repository):
    version = repository.fetch_version('bundler', '1.15.4')
    assert version.runtime_dependencies == []
    assert version.development_dependencies == [
        Dependency('automatiek'),
        Dependency('mustache'),
        Dependency('rake'),
        Dependency('rdiscount'),
        Dependency('ronn'),
        Dependency('rspec')
    ]


@vcr.use_cassette('cassettes/ruby_package_version_without_development_dependencies.yaml')
def test_fetch_version_without_development_dependencies(repository):
    version = repository.fetch_version('rails', '5.1.4')
    assert version.runtime_dependencies == [
        Dependency('actioncable'),
        Dependency('actionmailer'),
        Dependency('actionpack'),
        Dependency('actionview'),
        Dependency('activejob'),
        Dependency('activemodel'),
        Dependency('activerecord'),
        Dependency('activesupport'),
        Dependency('bundler'),
        Dependency('railties'),
        Dependency('sprockets-rails')
    ]
    assert version.development_dependencies == []
