import pytest

from app.platforms.jvm.package_name import JvmPackageName


@pytest.fixture
def name():
    return JvmPackageName('org.spire-math', 'kind-projector_2.10')


def test_str(name):
    assert str(name) == 'org.spire-math:kind-projector_2.10'
    assert repr(name) == 'org.spire-math:kind-projector_2.10'


def test_group_id(name):
    assert name.group_id == 'org.spire-math'


def test_artifact_id(name):
    assert name.artifact_id == 'kind-projector_2.10'


def test_group_path(name):
    assert name.group_path == 'org/spire-math'


def test_artifact_id_has_scala_version():
    name = JvmPackageName('org.spire-math', 'kind-projector_2.10')
    assert name.artifact_id_with_default_scala_version('2.11') == 'kind-projector_2.10'


def test_artifact_id_does_not_have_scala_version():
    name = JvmPackageName('org.spire-math', 'kind-projector')
    assert name.artifact_id_with_default_scala_version('2.11') == 'kind-projector_2.11'
