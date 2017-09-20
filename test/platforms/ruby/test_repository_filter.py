import pytest

from test import *
from app.github_repository import *
from app.platforms.ruby.repository_filter import *


@pytest.fixture
def ruby_repository():
    return GithubRepository('toptal', 'platform', http_compression=False)


@pytest.fixture
def python_repository():
    return GithubRepository('toptal', 'license-cop', http_compression=False)


@pytest.fixture
def ruby_filter():
    return RubyRepositoryFilter()


def dependency(name):
    return Dependency(name, Dependency.RUNTIME)


@VCR.use_cassette('ruby_repository_filter_match.yaml')
def test_matches_ruby_repository(ruby_filter, ruby_repository):
    assert ruby_filter.match(ruby_repository)


@VCR.use_cassette('ruby_repository_filter_mismatch.yaml')
def test_mismatches_python_repository(ruby_filter, python_repository):
    assert not ruby_filter.match(python_repository)


@VCR.use_cassette('ruby_repository_filter_dependencies.yaml')
def test_mismatches_python_repository(ruby_filter, ruby_repository):
    dependencies = ruby_filter.filter_dependencies(ruby_repository)
    assert len(dependencies) == 205

    assert dependency('rails') in dependencies
    assert dependency('pg') in dependencies
    assert dependency('elasticsearch') in dependencies
    assert dependency('elasticsearch-extensions') in dependencies
    assert dependency('chewy') in dependencies
    assert dependency('method_source') in dependencies
    assert dependency('parser') in dependencies
    assert dependency('unparser') in dependencies
    assert dependency('rollbar') in dependencies
    assert dependency('kaminari') in dependencies
    assert dependency('tzinfo-data') in dependencies
    assert dependency('time_zone_ext') in dependencies
    assert dependency('chronic') in dependencies
    assert dependency('business_time') in dependencies
    assert dependency('rack-rewrite') in dependencies
    assert dependency('hiredis') in dependencies
    assert dependency('redis-rails') in dependencies
    assert dependency('hairtrigger') in dependencies
    assert dependency('actionpack-action_caching') in dependencies
    assert dependency('rails-observers') in dependencies
    assert dependency('rails_autolink') in dependencies
    assert dependency('seedbank') in dependencies
    assert dependency('oj') in dependencies
    assert dependency('oj_mimic_json') in dependencies
    assert dependency('slim-rails') in dependencies
    assert dependency('tilt') in dependencies
    assert dependency('kramdown') in dependencies
    assert dependency('liquid') in dependencies
    assert dependency('rabl') in dependencies
    assert dependency('active_model_serializers') in dependencies
    assert dependency('fog-aws') in dependencies
    assert dependency('mimemagic') in dependencies
    assert dependency('carrierwave') in dependencies
    assert dependency('graphitti') in dependencies
    assert dependency('draper') in dependencies
    assert dependency('active_data') in dependencies
    assert dependency('uuidtools') in dependencies
    assert dependency('disqus_api') in dependencies
    assert dependency('hackerrank') in dependencies
    assert dependency('grape') in dependencies
    assert dependency('savon') in dependencies
    assert dependency('paypal-sdk-rest') in dependencies
    assert dependency('apnotic') in dependencies
    assert dependency('doorkeeper') in dependencies
    assert dependency('activeresource') in dependencies
    assert dependency('activemodel-serializers-xml') in dependencies
    assert dependency('hyperwallet-rb') in dependencies
    assert dependency('twilio-ruby') in dependencies
    assert dependency('slack-notifier') in dependencies
    assert dependency('roadie') in dependencies
    assert dependency('sass-rails') in dependencies
    assert dependency('webpack-assets') in dependencies
    assert dependency('addressable') in dependencies
    assert dependency('faraday') in dependencies
    assert dependency('faraday_middleware') in dependencies
    assert dependency('typhoeus') in dependencies
    assert dependency('chameleon-sdk') in dependencies
    assert dependency('user_agent_parser') in dependencies
    assert dependency('memoist') in dependencies
    assert dependency('config') in dependencies
    assert dependency('rubyzip') in dependencies
    assert dependency('rightsignature') in dependencies
    assert dependency('restforce') in dependencies
    assert dependency('levenshtein-ffi') in dependencies
    assert dependency('meta-tags') in dependencies
    assert dependency('globalize') in dependencies
    assert dependency('globalize-accessors') in dependencies
    assert dependency('aws-sdk') in dependencies
    assert dependency('utf8-cleaner') in dependencies
    assert dependency('premailer') in dependencies
    assert dependency('lograge') in dependencies
    assert dependency('activejob-retry') in dependencies
    assert dependency('parallel') in dependencies
    assert dependency('net-sftp') in dependencies
    assert dependency('gpgme') in dependencies
    assert dependency('bootsnap') in dependencies
    assert dependency('clockwork') in dependencies
    assert dependency('rack-cors') in dependencies
    assert dependency('blog') in dependencies
    assert dependency('public') in dependencies
    assert dependency('community') in dependencies
    assert dependency('skill_vs_skill') in dependencies
    assert dependency('roadtrip') in dependencies
    assert dependency('ab_testing') in dependencies
    assert dependency('stripe') in dependencies
    assert dependency('paper_trail') in dependencies
    assert dependency('virtus') in dependencies
    assert dependency('accrual_accounting') in dependencies
    assert dependency('nokogiri') in dependencies
    assert dependency('graphql') in dependencies
    assert dependency('graphql-batch') in dependencies
    assert dependency('retina_tag') in dependencies
    assert dependency('gon') in dependencies
    assert dependency('simple_form') in dependencies
    assert dependency('devise') in dependencies
    assert dependency('cancancan') in dependencies
    assert dependency('omniauth-google-oauth2') in dependencies
    assert dependency('jwt') in dependencies
    assert dependency('bcrypt') in dependencies
    assert dependency('mini_magick') in dependencies
    assert dependency('wkhtmltopdf-binary-edge') in dependencies
    assert dependency('acts_as_list') in dependencies
    assert dependency('posix-spawn') in dependencies
    assert dependency('delayed_job') in dependencies
    assert dependency('delayed_job_active_record') in dependencies
    assert dependency('daemons') in dependencies
    assert dependency('maxminddb') in dependencies
    assert dependency('geokit') in dependencies
    assert dependency('io-extra') in dependencies
    assert dependency('newrelic_rpm') in dependencies
    assert dependency('global_phone') in dependencies
    assert dependency('colorize') in dependencies
    assert dependency('ruby-progressbar') in dependencies
    assert dependency('email_reply_parser') in dependencies
    assert dependency('analytics-ruby') in dependencies
    assert dependency('hubspot-ruby') in dependencies
    assert dependency('mail') in dependencies
    assert dependency('gretel') in dependencies
    assert dependency('inline_svg') in dependencies
    assert dependency('lever_postings') in dependencies
    assert dependency('holidays') in dependencies
    assert dependency('roo') in dependencies
    assert dependency('browser') in dependencies
    assert dependency('sqreen') in dependencies
    assert dependency('whois-parser') in dependencies
    assert dependency('public_suffix') in dependencies
    assert dependency('neo_form') in dependencies
    assert dependency('neo_list') in dependencies
    assert dependency('rubyXL') in dependencies
    assert dependency('monolith') in dependencies
    assert dependency('petri') in dependencies
    assert dependency('pry-rails') in dependencies
    assert dependency('pry-rescue') in dependencies
    assert dependency('pry-stack_explorer') in dependencies
    assert dependency('pry-byebug') in dependencies
    assert dependency('pry-doc') in dependencies
    assert dependency('factory_girl') in dependencies
    assert dependency('timecop') in dependencies
    assert dependency('ffaker') in dependencies
    assert dependency('knapsack') in dependencies
    assert dependency('gherkin') in dependencies
    assert dependency('awesome_print') in dependencies
    assert dependency('hashdiff') in dependencies
    assert dependency('ruby-prof') in dependencies
    assert dependency('ruby-prof-flamegraph') in dependencies
    assert dependency('database_cleaner') in dependencies
    assert dependency('parallel_tests') in dependencies
    assert dependency('get_process_mem') in dependencies
    assert dependency('stackprof') in dependencies
    assert dependency('rspec') in dependencies
    assert dependency('rspec-rails') in dependencies
    assert dependency('rspec-its') in dependencies
    assert dependency('rspec-activemodel-mocks') in dependencies
    assert dependency('rspec-collection_matchers') in dependencies
    assert dependency('rspec_junit_formatter') in dependencies
    assert dependency('capybara') in dependencies
    assert dependency('require_all') in dependencies
    assert dependency('vcr') in dependencies
    assert dependency('webmock') in dependencies
    assert dependency('simplecov') in dependencies
    assert dependency('email_spec') in dependencies
    assert dependency('json_spec') in dependencies
    assert dependency('fuubar') in dependencies
    assert dependency('stripe-ruby-mock') in dependencies
    assert dependency('equivalent-xml') in dependencies
    assert dependency('nokogiri-pretty') in dependencies
    assert dependency('top-rspec-matchers') in dependencies
    assert dependency('db-query-matchers') in dependencies
    assert dependency('shoulda-matchers') in dependencies
    assert dependency('rails-controller-testing') in dependencies
    assert dependency('cucumber') in dependencies
    assert dependency('headless') in dependencies
    assert dependency('puffing-billy') in dependencies
    assert dependency('selenium-webdriver') in dependencies
    assert dependency('spring-commands-cucumber') in dependencies
    assert dependency('thin') in dependencies
    assert dependency('watir') in dependencies
    assert dependency('watir-dom-wait') in dependencies
    assert dependency('watir-rails') in dependencies
    assert dependency('watir-scroll') in dependencies
    assert dependency('watirsome') in dependencies
    assert dependency('webdriver-highlighter') in dependencies
    assert dependency('spring') in dependencies
    assert dependency('spring-commands-rspec') in dependencies
    assert dependency('spring-commands-rubocop') in dependencies
    assert dependency('guard') in dependencies
    assert dependency('guard-rspec') in dependencies
    assert dependency('guard-livereload') in dependencies
    assert dependency('terminal-notifier-guard') in dependencies
    assert dependency('rubocop') in dependencies
    assert dependency('rubocop-rspec') in dependencies
    assert dependency('brakeman') in dependencies
    assert dependency('foreman') in dependencies
    assert dependency('autodoc') in dependencies
    assert dependency('better_errors') in dependencies
    assert dependency('binding_of_caller') in dependencies
    assert dependency('bullet') in dependencies
    assert dependency('overcommit') in dependencies
    assert dependency('benchmark-ips') in dependencies
    assert dependency('rack-mini-profiler') in dependencies
    assert dependency('yard') in dependencies
    assert dependency('yard-junk') in dependencies
    assert dependency('redcarpet') in dependencies
    assert dependency('github-markup') in dependencies
    assert dependency('ruby-graphviz') in dependencies
