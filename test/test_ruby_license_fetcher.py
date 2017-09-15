import vcr
import pytest

from app.ruby_license_fetcher import RubyLicenseFetcher


@pytest.fixture
def fetcher(): return RubyLicenseFetcher(http_compression=False)


@vcr.use_cassette('cassettes/ruby_gem_has_one_license.yaml')
def test_fetches_licenses_when_gem_has_one_license(fetcher):
    licenses = fetcher.fetch_licenses('rubocop', '0.49.1')
    assert licenses == ['MIT']


@vcr.use_cassette('cassettes/ruby_gem_has_no_license.yaml')
def test_fetches_licenses_when_gem_has_no_license(fetcher):
    licenses = fetcher.fetch_licenses('coulda', '0.7.1')
    assert licenses == []


@vcr.use_cassette('cassettes/ruby_gem_has_multiple_licenses.yaml')
def test_fetches_licenses_when_gem_has_multiple_licenses(fetcher):
    licenses = fetcher.fetch_licenses('rails', '5.1.4')
    assert licenses == ['MIT', 'Apache']


@vcr.use_cassette('cassettes/ruby_gem_name_does_not_exist.yaml')
def test_fetches_licenses_whem_gem_name_does_not_exist(fetcher):
    licenses = fetcher.fetch_licenses('foobar666', '666')
    assert licenses is None


@vcr.use_cassette('cassettes/ruby_gem_version_does_not_exist.yaml')
def test_fetches_licenses_whem_gem_name_does_not_exist(fetcher):
    licenses = fetcher.fetch_licenses('rails', '666')
    assert licenses is None
