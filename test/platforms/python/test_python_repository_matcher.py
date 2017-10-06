import pytest
from textwrap import dedent

from test import *
from app.dependency import *
from app.github.repository import *
from app.platforms.python.repository_matcher import *


@pytest.fixture
def nodejs_repository():
    return GithubRepository.from_url(
        'https://github.com/browserify/browserify',
        http_compression=False
    )


@pytest.fixture
def requirements_repository():
    return GithubRepository.from_url(
        'https://github.com/alanhamlett/pip-update-requirements',
        http_compression=False
    )


@pytest.fixture
def pipfile_repository():
    return GithubRepository('toptal', 'license-cop', http_compression=False)


@pytest.fixture
def matcher():
    return PythonRepositoryMatcher()


def test_parse_requirements_file():
    data = dedent('''\
        pandas~=0.20.2
        httplib2~=0.10.2
            pyOpenSSL~=16.2.0
        google-cloud~=0.23.0
        google-api-python-client~=1.6.2

        grpcio==1.4.0
        oauth2client~=4.1.2
        googleads==6.0.0

        # This is a comment
        luigi==2.6.2
        ruamel.yaml==0.15.18
        newrelic~=2.90.0.75
        -e ./foobar-common/
        -e ./foobar-avro/
        -e ./foobar-api/
        -e ./foobar-csv/
        -e ./foobar-etl/
        -e ./foobar-orchestration/
        -e ./foobar-validation/
        -e ./foobar-chronos/
        wheel

    ''')

    assert parse_requirements_file(data, DependencyKind.DEVELOPMENT) == [
        Dependency.development('pandas'),
        Dependency.development('httplib2'),
        Dependency.development('pyOpenSSL'),
        Dependency.development('google-cloud'),
        Dependency.development('google-api-python-client'),
        Dependency.development('grpcio'),
        Dependency.development('oauth2client'),
        Dependency.development('googleads'),
        Dependency.development('luigi'),
        Dependency.development('ruamel.yaml'),
        Dependency.development('newrelic'),
        Dependency.development('wheel')
    ]


def test_parse_pipfile():
    data = dedent('''\
        [[source]]
        url = 'https://pypi.python.org/simple'
        verify_ssl = true

        [requires]
        python_version = '2.7'

        [packages]
        requests = { extras = ['socks'] }
        records = '>0.5.0'
        django = { git = 'https://github.com/django/django.git', ref = '1.11.4', editable = true }

        [dev-packages]
        pytest = ">=2.8.0"
        codecov = "*"
        "pytest-httpbin" = "==0.0.7"
        "pytest-mock" = "*"
        "pytest-cov" = "*"
        "pytest-xdist" = "*"
        alabaster = "*"
        "readme-renderer" = "*"
        sphinx = "<=1.5.5"
        pysocks = "*"
        docutils = "*"
        "flake8" = "*"
        tox = "*"
        detox = "*"
        httpbin = "==0.5.0"
    ''')

    (runtime, development) = parse_pipfile(data)

    assert runtime == [
        Dependency.runtime('requests'),
        Dependency.runtime('records'),
        Dependency.runtime('django')
    ]
    assert development == [
        Dependency.development('pytest'),
        Dependency.development('codecov'),
        Dependency.development('pytest-httpbin'),
        Dependency.development('pytest-mock'),
        Dependency.development('pytest-cov'),
        Dependency.development('pytest-xdist'),
        Dependency.development('alabaster'),
        Dependency.development('readme-renderer'),
        Dependency.development('sphinx'),
        Dependency.development('pysocks'),
        Dependency.development('docutils'),
        Dependency.development('flake8'),
        Dependency.development('tox'),
        Dependency.development('detox'),
        Dependency.development('httpbin')
    ]


@VCR.use_cassette('python_repository_matcher_match_repository_with_requirements.yaml')
def test_match_repository_with_requirements(matcher, requirements_repository):
    assert matcher.match(requirements_repository) is not None


@VCR.use_cassette('python_repository_matcher_match_repository_with_pipfile.yaml')
def test_match_repository_with_pipfile(matcher, pipfile_repository):
    assert matcher.match(pipfile_repository) is not None


@VCR.use_cassette('python_repository_matcher_mismatch_repository_without_requirements_nor_pipfile.yaml')
def test_mismatch_repository_without_requirements_nor_pipfile(matcher, nodejs_repository):
    assert matcher.match(nodejs_repository) is None


@VCR.use_cassette('python_repository_matcher_extract_package_descriptor_from_requirements_files.yaml')
def test_extract_package_descriptor_from_requirements_files(matcher, requirements_repository):
    match = matcher.match(requirements_repository)

    descriptors = match.package_descriptors()
    descriptor = descriptors[0]

    assert descriptor.platform == 'Python'
    assert descriptor.repository == requirements_repository
    assert descriptor.paths == ['requirements.txt', 'dev-requirements.txt']
    assert descriptor.runtime_dependencies == [
        Dependency.runtime('click')
    ]
    assert descriptor.development_dependencies == [
        Dependency.development('coverage'),
        Dependency.development('mock'),
        Dependency.development('nose'),
        Dependency.development('nose-capturestderr'),
        Dependency.development('nose-exclude')
    ]


@VCR.use_cassette('python_repository_matcher_extract_package_descriptor_from_pipfile.yaml')
def test_extract_package_descriptor_from_pipfile(matcher, pipfile_repository):
    match = matcher.match(pipfile_repository)

    descriptors = match.package_descriptors()
    descriptor = descriptors[0]

    assert descriptor.platform == 'Python'
    assert descriptor.repository == pipfile_repository
    assert descriptor.paths == ['Pipfile']
    assert descriptor.runtime_dependencies == [
        Dependency.runtime('requests')
    ]
    assert descriptor.development_dependencies == [
        Dependency.development('pytest'),
        Dependency.development('vcrpy'),
        Dependency.development('pytest-mock')
    ]
