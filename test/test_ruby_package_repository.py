import vcr
import pytest
import requests

from app.ruby_package_repository import *


@pytest.fixture
def repository(): return RubyPackageRepository(http_compression=False)


@vcr.use_cassette('cassettes/ruby_package_repository_version.yaml')
def test_fetch_version(repository):
    version = repository.fetch_version('rails', '3.2.22')
    assert version.name == 'rails'
    assert version.number == '3.2.22'
    assert version.licenses == ['MIT']
    assert version.dependencies == [
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


@vcr.use_cassette('cassettes/ruby_package_repository_latest_version.yaml')
def test_fetch_latest_version(repository):
    version = repository.fetch_latest_version('rails')
    assert version.name == 'rails'
    assert version.number == '5.1.4'
    assert version.licenses == ['MIT']
    assert version.dependencies == [
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


@vcr.use_cassette('cassettes/ruby_package_version_without_dependencies.yaml')
def test_fetch_version_without_dependencies(repository):
    version = repository.fetch_version('rdiscount', '2.2.0.1')
    assert version.dependencies == []
