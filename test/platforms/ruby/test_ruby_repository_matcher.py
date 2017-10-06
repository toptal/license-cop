import pytest

from test import *
from app.github.repository import *
from app.platforms.ruby.repository_matcher import *


@pytest.fixture
def ruby_repository():
    return GithubRepository.from_url(
        'https://github.com/rails/rails',
        http_compression=False
    )


@pytest.fixture
def python_repository():
    return GithubRepository('toptal', 'license-cop', http_compression=False)


@pytest.fixture
def matcher():
    return RubyRepositoryMatcher()


@VCR.use_cassette('ruby_repository_matcher_match_repository_with_gemfile.yaml')
def test_match_repository_with_gemfile(matcher, ruby_repository):
    assert matcher.match(ruby_repository) is not None


@VCR.use_cassette('ruby_repository_matcher_mismatch_repository_without_gemfile.yaml')
def test_mismatch_repository_without_gemfile(matcher, python_repository):
    assert matcher.match(python_repository) is None


@VCR.use_cassette('ruby_repository_matcher_gemfile_package_descriptor.yaml')
def test_gemfile_package_descriptor(matcher, ruby_repository):
    match = matcher.match(ruby_repository)

    descriptors = match.package_descriptors()
    descriptor = descriptors[0]

    assert descriptor.platform == 'Ruby'
    assert descriptor.repository == ruby_repository
    assert descriptor.paths == ['Gemfile']

    assert descriptor.runtime_dependencies == [
        Dependency.runtime('arel'),
        Dependency.runtime('rake'),
        Dependency.runtime('mocha'),
        Dependency.runtime('capybara'),
        Dependency.runtime('rack-cache'),
        Dependency.runtime('jquery-rails'),
        Dependency.runtime('coffee-rails'),
        Dependency.runtime('sass-rails'),
        Dependency.runtime('turbolinks'),
        Dependency.runtime('bcrypt'),
        Dependency.runtime('uglifier'),
        Dependency.runtime('json'),
        Dependency.runtime('rubocop'),
        Dependency.runtime('rb-inotify'),
        Dependency.runtime('sdoc'),
        Dependency.runtime('redcarpet'),
        Dependency.runtime('w3c_validators'),
        Dependency.runtime('kindlerb'),
        Dependency.runtime('dalli'),
        Dependency.runtime('listen'),
        Dependency.runtime('libxml-ruby'),
        Dependency.runtime('erubis'),
        Dependency.runtime('bootsnap'),
        Dependency.runtime('resque'),
        Dependency.runtime('resque-scheduler'),
        Dependency.runtime('sidekiq'),
        Dependency.runtime('sucker_punch'),
        Dependency.runtime('delayed_job'),
        Dependency.runtime('queue_classic'),
        Dependency.runtime('sneakers'),
        Dependency.runtime('que'),
        Dependency.runtime('backburner'),
        Dependency.runtime('delayed_job_active_record'),
        Dependency.runtime('sequel'),
        Dependency.runtime('puma'),
        Dependency.runtime('em-hiredis'),
        Dependency.runtime('hiredis'),
        Dependency.runtime('redis'),
        Dependency.runtime('websocket-client-simple'),
        Dependency.runtime('blade'),
        Dependency.runtime('blade-sauce_labs_plugin'),
        Dependency.runtime('sprockets-export'),
        Dependency.runtime('aws-sdk-s3'),
        Dependency.runtime('google-cloud-storage'),
        Dependency.runtime('azure-storage'),
        Dependency.runtime('mini_magick'),
        Dependency.runtime('minitest-bisect'),
        Dependency.runtime('stackprof'),
        Dependency.runtime('byebug'),
        Dependency.runtime('benchmark-ips'),
        Dependency.runtime('nokogiri'),
        Dependency.runtime('racc'),
        Dependency.runtime('sqlite3'),
        Dependency.runtime('pg'),
        Dependency.runtime('mysql2'),
        Dependency.runtime('activerecord-jdbcsqlite3-adapter'),
        Dependency.runtime('activerecord-jdbcmysql-adapter'),
        Dependency.runtime('activerecord-jdbcpostgresql-adapter'),
        Dependency.runtime('activerecord-jdbcsqlite3-adapter'),
        Dependency.runtime('activerecord-jdbcmysql-adapter'),
        Dependency.runtime('activerecord-jdbcpostgresql-adapter'),
        Dependency.runtime('psych'),
        Dependency.runtime('ruby-oci8'),
        Dependency.runtime('activerecord-oracle_enhanced-adapter'),
        Dependency.runtime('ibm_db'),
        Dependency.runtime('tzinfo-data'),
        Dependency.runtime('wdm')
    ]
