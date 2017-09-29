import pytest
import requests

from test import *
from app.package_registry import *
from app.platforms.python.package_registry import *
from app.dependency import *


@pytest.fixture
def registry(): return PythonPackageRegistry(http_compression=False)


def test_parse_dependency_with_version_without_extra_with_semicolon_as_runtime():
    d = parse_dependency('pyOpenSSL (>=1.5.2)')
    assert d.name == 'pyOpenSSL'
    assert d.is_runtime


def test_parse_dependency_with_version_without_extra_with_semicolon_as_runtime():
    d = parse_dependency('pyOpenSSL (>=1.5.2);')
    assert d.name == 'pyOpenSSL'
    assert d.is_runtime


def test_parse_dependency_with_greater_or_equal_version():
    d = parse_dependency('pyOpenSSL (>=1.5.2)')
    assert d.name == 'pyOpenSSL'


def test_parse_dependency_with_less_version():
    d = parse_dependency('pyOpenSSL (<1.5.2)')
    assert d.name == 'pyOpenSSL'


def test_parse_dependency_with_different_version():
    d = parse_dependency('pyOpenSSL (!=1.5.7)')
    assert d.name == 'pyOpenSSL'


def test_parse_dependency_with_combined_version():
    d = parse_dependency('pyOpenSSL (<1.23,>=1.21.1,!=1.22.3)')
    assert d.name == 'pyOpenSSL'


def test_parse_dependency_without_version_without_extra_without_semicolon_as_runtime():
    d = parse_dependency('pyOpenSSL')
    assert d.name == 'pyOpenSSL'
    assert d.is_runtime


def test_parse_dependency_without_version_without_extra_with_semicolon_as_runtime():
    d = parse_dependency('pyOpenSSL;')
    assert d.name == 'pyOpenSSL'
    assert d.is_runtime


def test_parse_dependency_with_version_with_unrecognized_extra_as_runtime():
    d = parse_dependency("pyOpenSSL (>=0.14); extra == 'security'")
    assert d.name == 'pyOpenSSL'
    assert d.is_runtime


def test_parse_dependency_with_version_with_test_extra_as_development():
    d = parse_dependency("pytest (>=3.0.1); extra == 'test'")
    assert d.name == 'pytest'
    assert d.is_development


def test_parse_dependency_with_version_with_tests_extra_as_development():
    d = parse_dependency("pytest (>=3.0.1); extra == 'tests'")
    assert d.name == 'pytest'
    assert d.is_development


def test_parse_dependency_with_version_with_testing_extra_as_development():
    d = parse_dependency("pytest (>=3.0.1); extra == 'testing'")
    assert d.name == 'pytest'
    assert d.is_development


def test_parse_dependency_with_version_with_doc_extra_as_development():
    d = parse_dependency("pytest (>=3.0.1); extra == 'doc'")
    assert d.name == 'pytest'
    assert d.is_development


def test_parse_dependency_with_version_with_docs_extra_as_development():
    d = parse_dependency("pytest (>=3.0.1); extra == 'docs'")
    assert d.name == 'pytest'
    assert d.is_development


def test_parse_dependency_with_version_with_dev_extra_as_development():
    d = parse_dependency("pytest (>=3.0.1); extra == 'dev'")
    assert d.name == 'pytest'
    assert d.is_development


def test_parse_dependency_with_version_with_development_extra_as_development():
    d = parse_dependency("pytest (>=3.0.1); extra == 'development'")
    assert d.name == 'pytest'
    assert d.is_development


def test_parse_dependency_with_version_with_devel_extra_as_development():
    d = parse_dependency("pytest (>=3.0.1); extra == 'devel'")
    assert d.name == 'pytest'
    assert d.is_development


def test_parse_dependency_with_version_with_debug_extra_as_development():
    d = parse_dependency("pytest (>=3.0.1); extra == 'debug'")
    assert d.name == 'pytest'
    assert d.is_development


def test_parse_dependency_with_version_with_debugging_extra_as_development():
    d = parse_dependency("pytest (>=3.0.1); extra == 'debugging'")
    assert d.name == 'pytest'
    assert d.is_development


def test_parse_dependency_without_version_with_unrecognized_extra_as_runtime():
    d = parse_dependency("pyOpenSSL; extra == 'foobar'")
    assert d.name == 'pyOpenSSL'
    assert d.is_runtime


def test_parse_dependency_without_version_with_recognized_extra_as_development():
    d = parse_dependency("pyOpenSSL; extra == 'test'")
    assert d.name == 'pyOpenSSL'
    assert d.is_development


def test_parse_dependency_with_double_quotes_extra():
    d = parse_dependency('pyOpenSSL; extra == "test"')
    assert d.name == 'pyOpenSSL'
    assert d.is_development


def test_parse_dependency_with_escaped_double_quotes_extra():
    d = parse_dependency('pyOpenSSL; extra == \\"test\\"')
    assert d.name == 'pyOpenSSL'
    assert d.is_development


def test_parse_dependency_with_other_checks_and_extra_at_end():
    d = parse_dependency(
        "win-inet-pton; sys_platform == \"win32\" and "
        "(python_version == \"2.7\" or python_version == \"2.6\") and extra == 'test'"
    )
    assert d.name == 'win-inet-pton'
    assert d.is_development


def test_parse_dependency_with_other_checks_and_extra_at_beginning():
    d = parse_dependency(
        "win-inet-pton; extra == 'test' and sys_platform == \"win32\" and "
        "(python_version == \"2.7\" or python_version == \"2.6\")"
    )
    assert d.name == 'win-inet-pton'
    assert d.is_development


def test_parse_dependency_with_other_checks_and_extra_in_middle():
    d = parse_dependency(
        "win-inet-pton; sys_platform == \"win32\" and extra == 'test' and "
        "(python_version == \"2.7\" or python_version == \"2.6\")"
    )
    assert d.name == 'win-inet-pton'
    assert d.is_development


def test_parse_dependency_with_underscores_in_the_name():
    d = parse_dependency('py_Open_SSL; extra == "test"')
    assert d.name == 'py_Open_SSL'
    assert d.is_development


def test_parse_dependency_with_dashes_in_the_name():
    d = parse_dependency('py-Open-SSL; extra == "test"')
    assert d.name == 'py-Open-SSL'
    assert d.is_development


def test_parse_dependency_with_dots_in_the_name():
    d = parse_dependency('py.Open.SSL; extra == "test"')
    assert d.name == 'py.Open.SSL'
    assert d.is_development


def test_raise_exception_if_dependency_could_not_be_parsed():
    string = '$%^&'
    with pytest.raises(Exception) as e:
        parse_dependency(string)
    assert str(e.value) == 'Could not parse dependency: {0}'.format(string)


@VCR.use_cassette('python_package_registry_fetch_version.yaml')
def test_fetch_version(registry):
    version = registry.fetch_version('pyOpenSSL', '17.2.0')
    assert version.name == 'pyOpenSSL'
    assert version.number == '17.2.0'
    assert version.licenses == ['Apache License, Version 2.0']
    assert version.runtime_dependencies == [
        Dependency.runtime('six'),
        Dependency.runtime('cryptography')
    ]
    assert version.development_dependencies == [
        Dependency.development('pytest'),
        Dependency.development('pretend'),
        Dependency.development('flaky'),
        Dependency.development('sphinx-rtd-theme'),
        Dependency.development('sphinx')
    ]


@VCR.use_cassette('python_package_registry_fetch_latest_version.yaml')
def test_fetch_latest_version(registry):
    version = registry.fetch_latest_version('pyOpenSSL')
    assert version.name == 'pyOpenSSL'
    assert version.number == '17.3.0'
    assert version.licenses == ['Apache License, Version 2.0']
    assert version.runtime_dependencies == [
        Dependency.runtime('six'),
        Dependency.runtime('cryptography')
    ]
    assert version.development_dependencies == [
        Dependency.development('pytest'),
        Dependency.development('pretend'),
        Dependency.development('flaky'),
        Dependency.development('sphinx-rtd-theme'),
        Dependency.development('sphinx')
    ]


@VCR.use_cassette('python_package_registry_fetch_version_name_not_found.yaml')
def test_fetch_version_name_not_found(registry):
    with pytest.raises(PackageVersionNotFoundError) as e:
        registry.fetch_version('foobar666', '666')
    assert str(e.value) == (
        'Could not find package version foobar666:666. '
        '404 Client Error: Not Found (invalid name/version) '
        'for url: https://pypi.python.org/pypi/foobar666/666/json'
    )


@VCR.use_cassette('python_package_registry_fetch_version_number_not_found.yaml')
def test_fetch_version_number_not_found(registry):
    with pytest.raises(PackageVersionNotFoundError) as e:
        registry.fetch_version('requests', '666')
    assert str(e.value) == (
        'Could not find package version requests:666. '
        '404 Client Error: Not Found (invalid name/version) '
        'for url: https://pypi.python.org/pypi/requests/666/json'
    )


@VCR.use_cassette('python_package_registry_fetch_latest_version_name_not_found.yaml')
def test_fetch_latest_version_name_not_found(registry):
    with pytest.raises(PackageVersionNotFoundError) as e:
        registry.fetch_latest_version('foobar666')
    assert str(e.value) == (
        'Could not find package version foobar666:latest. '
        '404 Client Error: Not Found (no releases) '
        'for url: https://pypi.python.org/pypi/foobar666/json'
    )


@VCR.use_cassette('python_package_registry_fetch_version_without_development_dependencies.yaml')
def test_fetch_version_without_development_dependencies(registry):
    version = registry.fetch_version('pyOpenSSL', '16.0.0')
    assert version.runtime_dependencies == [
        Dependency.runtime('cryptography'),
        Dependency.runtime('six')
    ]
    assert version.development_dependencies == []


@VCR.use_cassette('python_package_registry_fetch_version_without_dependencies.yaml')
def test_fetch_version_without_runtime_dependencies(registry):
    version = registry.fetch_version('six', '1.11.0')
    assert version.runtime_dependencies == []
    assert version.development_dependencies == []


@VCR.use_cassette('python_fetch_version_discarding_extra_lines_from_license.yaml')
def test_fetch_version_discarding_extra_lines_from_license(registry):
    version = registry.fetch_version('flaky', '3.4.0')
    assert version.licenses == ['Apache License [...]']


@VCR.use_cassette('python_fetch_version_discarding_blank_lines_from_license.yaml')
def test_fetch_version_discarding_blank_lines_from_license(registry):
    version = registry.fetch_version('flaky', '3.4.0')
    assert version.licenses == ['Apache License [...]']


@VCR.use_cassette('python_fetch_version_discarding_empty_licenses.yaml')
def test_fetch_version_discarding_empty_licenses(registry):
    version = registry.fetch_version('setuptools', '36.5.0')
    assert version.licenses == []


@VCR.use_cassette('python_fetch_version_read_license_from_github_if_no_licenses.yaml')
def test_fetch_version_read_license_from_github_if_no_licenses(registry):
    version = registry.fetch_version('mock', '2.0.0')
    assert version.licenses == ['BSD-2-Clause']
