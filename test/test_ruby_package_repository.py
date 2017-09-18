import vcr
import pytest

from app.ruby_package_repository import *


@pytest.fixture
def repository(): return RubyPackageRepository(http_compression=False)


@vcr.use_cassette('cassettes/ruby_package_name_does_not_exist.yaml')
def test_return_none_when_package_name_does_not_exist(repository):
    package = repository.fetch_package('foobar666', '666')
    assert package is None


@vcr.use_cassette('cassettes/ruby_package_version_does_not_exist.yaml')
def test_return_none_when_package_version_does_not_exist(repository):
    package = repository.fetch_package('rails', '666')
    assert package is None


@vcr.use_cassette('cassettes/ruby_package_has_one_license.yaml')
def test_fetch_licenses_when_package_has_one_license(repository):
    package = repository.fetch_package('rubocop', '0.49.1')
    assert package.licenses == ['MIT']


@vcr.use_cassette('cassettes/ruby_package_has_no_license.yaml')
def test_fetch_licenses_when_package_has_no_license(repository):
    package = repository.fetch_package('coulda', '0.7.1')
    assert package.licenses == []


@vcr.use_cassette('cassettes/ruby_package_has_multiple_licenses.yaml')
def test_fetch_licenses_when_package_has_multiple_licenses(repository):
    package = repository.fetch_package('rails', '5.1.4')
    assert package.licenses == ['MIT', 'Apache']


@vcr.use_cassette('cassettes/ruby_package_with_dependencies.yaml')
def test_fetch_dependencies_when_there_are_dependencies(repository):
    package = repository.fetch_package('rails', '5.1.4')
    assert package.dependencies == [
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


@vcr.use_cassette('cassettes/ruby_package_without_dependencies.yaml')
def test_fetch_dependencies_when_there_are_no_dependencies(repository):
    package = repository.fetch_package('rdiscount', '2.2.0.1')
    assert package.dependencies == []
