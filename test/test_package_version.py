import pytest

from app.package_version import *


def build_version(licenses):
    return PackageVersion(
        name='pytest',
        number='3.2.2',
        runtime_dependencies=[],
        development_dependencies=[],
        licenses=licenses
    )


def test_str_with_one_license():
    version = build_version(licenses=['MIT'])
    assert str(version) == 'pytest:3.2.2 → MIT'


def test_str_with_multiple_licenses():
    version = build_version(licenses=['MIT', 'BSD'])
    assert str(version) == 'pytest:3.2.2 → MIT, BSD'


def test_str_without_licenses():
    version = build_version(licenses=[])
    assert str(version) == 'pytest:3.2.2 → <no licenses found>'


def test_str_not_found_with_number():
    version = PackageVersionNotFound('pytest', '3.2.2')
    assert str(version) == 'pytest:3.2.2 → <version not found on registry>'


def test_str_not_found_without_number():
    version = PackageVersionNotFound('pytest')
    assert str(version) == 'pytest:latest → <version not found on registry>'
