import pytest

from app.package_version import PackageVersion
from app.reverse_dependency import ReverseDependency
from app.dependency_resolution import DependencyResolution
from app.dependency import DependencyKind


@pytest.fixture
def version(name='rails'): return PackageVersion(name, '5.1.4', [], [], [])


@pytest.fixture
def dependency(version): return ReverseDependency(version)


@pytest.fixture
def resolution(version): return DependencyResolution.runtime(version)


def test_name_and_number(dependency):
    assert dependency.name == 'rails'
    assert dependency.number == '5.1.4'


def test_add_runtime_reference(dependency, resolution):
    dependency.add_reference(resolution, DependencyKind.RUNTIME)
    assert dependency.runtime_references == [resolution]
    assert dependency.development_references == []


def test_add_development_reference(dependency, resolution):
    dependency.add_reference(resolution, DependencyKind.DEVELOPMENT)
    assert dependency.runtime_references == []
    assert dependency.development_references == [resolution]
