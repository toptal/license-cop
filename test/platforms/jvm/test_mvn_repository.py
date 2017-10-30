import pytest

from test import *
from app.platforms.jvm.mvn_repository import MvnRepository
from app.platforms.jvm.package_name import JvmPackageName


@pytest.fixture
def mvn_repository():
    return MvnRepository(http_compression=False)


@VCR.use_cassette('mvn_repository_fetch_licenses_when_artifact_does_not_exist.yaml')
def test_fetch_licenses_when_artifact_does_not_exist(mvn_repository):
    name = JvmPackageName('org.example', 'foobar', '2.11.7-RC1')
    licenses = mvn_repository.fetch_licenses(name, '1.0.3')
    assert licenses == []


@VCR.use_cassette('mvn_repository_fetch_licenses_when_artifact_has_one_license.yaml')
def test_fetch_licenses_when_artifact_has_one_license(mvn_repository):
    name = JvmPackageName('org.scala-sbt', 'zinc', '2.11.7-RC1')
    licenses = mvn_repository.fetch_licenses(name, '1.0.3')
    assert licenses == ['BSD']


@VCR.use_cassette('mvn_repository_fetch_licenses_when_artifact_has_multiple_licenses.yaml')
def test_fetch_licenses_when_artifact_has_multiple_licenses(mvn_repository):
    name = JvmPackageName('org.eclipse.jetty', 'jetty-webapp', '2.11.7-RC1')
    licenses = mvn_repository.fetch_licenses(name, '9.4.7.v20170914')
    assert licenses == ['Apache 2.0', 'EPL 1.0']
