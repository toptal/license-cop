import pytest

from app.dependency import *


def test_runtime_kind_str():
    assert str(DependencyKind.RUNTIME) == 'runtime'


def test_development_kind_str():
    assert str(DependencyKind.DEVELOPMENT) == 'development'


def test_dependency_with_number_str():
    dependency = Dependency.runtime('pytest', '3.5.0')
    assert str(dependency) == '[runtime] pytest:3.5.0'


def test_dependency_without_number_str():
    dependency = Dependency.runtime('pytest')
    assert str(dependency) == '[runtime] pytest:latest'


def test_development_dependency__str():
    dependency = Dependency.development('pytest')
    assert str(dependency) == '[development] pytest:latest'
