import pytest

from app.package_version import *


def build_version(name='pytest', number='3.2.2', licenses=[]):
    return PackageVersion(
        name=name,
        number=number,
        runtime_dependencies=[],
        development_dependencies=[],
        licenses=licenses
    )


def test_id_without_number():
    v = build_version(number=None)
    assert v.id == 'pytest:latest'


def test_id_with_number():
    v = build_version()
    assert v.id == 'pytest:3.2.2'


def test_formatted_number_with_number():
    v = build_version()
    assert v.formatted_number == '3.2.2'


def test_formatted_number_without_number():
    v = build_version(number=None)
    assert v.formatted_number == 'latest'


def test_formatted_licenses_with_one_license():
    v = build_version(licenses=['MIT'])
    assert v.formatted_licenses == 'MIT'


def test_formatted_number_with_multiple_licenses():
    v = build_version(licenses=['MIT', 'BSD'])
    assert v.formatted_licenses == 'MIT|BSD'


def test_formatted_number_without_licenses():
    v = build_version()
    assert v.formatted_licenses == '<no licenses found>'


def test_str_with_number():
    v = build_version()
    assert str(v) == 'pytest:3.2.2'


def test_str_without_number():
    v = build_version(number=None)
    assert str(v) == 'pytest:latest'


def test_repr_with_one_license():
    v = build_version(licenses=['MIT'])
    assert repr(v) == 'pytest:3.2.2 → MIT'


def test_repr_with_multiple_licenses():
    v = build_version(licenses=['MIT', 'BSD'])
    assert repr(v) == 'pytest:3.2.2 → MIT|BSD'


def test_repr_without_licenses():
    v = build_version(licenses=[])
    assert repr(v) == 'pytest:3.2.2 → <no licenses found>'


def test_repr_not_found_with_number():
    v = PackageVersionNotFound('pytest', '3.2.2')
    assert repr(v) == 'pytest:3.2.2 → <version not found on registry>'


def test_repr_not_found_without_number():
    v = PackageVersionNotFound('pytest')
    assert repr(v) == 'pytest:latest → <version not found on registry>'
