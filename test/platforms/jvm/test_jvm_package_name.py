import pytest

from app.platforms.jvm.package_name import JvmPackageName


def test_group_id_and_path():
    name = JvmPackageName('org.spire-math', 'kind-projector_2.10')
    assert name.group_id == 'org.spire-math'
    assert name.group_path == 'org/spire-math'


def test_artifact_id():
    name = JvmPackageName('org.spire-math', 'kind-projector_2.10')
    assert name.artifact_id == 'kind-projector_2.10'


def test_artifact_id_with_scala_version_when_scala_version_is_explicit():
    name = JvmPackageName('org.spire-math', 'kind-projector', '2.10')
    assert name.artifact_id_with_scala_version == 'kind-projector_2.10'


def test_artifact_id_with_scala_version_when_scala_version_is_implicit():
    name = JvmPackageName('org.spire-math', 'kind-projector_2.10')
    assert name.artifact_id_with_scala_version == 'kind-projector_2.10'


def test_artifact_id_with_scala_version_when_scala_version_is_implicit_and_artifact_id_has_underscores():
    name = JvmPackageName('org.spire-math', 'kind_projector_2.10')
    assert name.artifact_id_with_scala_version == 'kind_projector_2.10'


def test_artifact_id_with_scala_version_when_scala_version_is_both_implicit_and_explicit():
    name = JvmPackageName('org.spire-math', 'kind-projector_2.10', '2.11')
    assert name.artifact_id_with_scala_version == 'kind-projector_2.10'


def test_artifact_id_with_scala_version_when_scala_version_is_none():
    name = JvmPackageName('org.spire-math', 'kind-projector')
    assert name.artifact_id_with_scala_version == 'kind-projector'


def test_artifact_id_without_scala_version_when_scala_version_is_explicit():
    name = JvmPackageName('org.spire-math', 'kind-projector', '2.10')
    assert name.artifact_id_without_scala_version == 'kind-projector'


def test_artifact_id_without_scala_version_when_scala_version_is_implicit():
    name = JvmPackageName('org.spire-math', 'kind-projector_2.10')
    assert name.artifact_id_without_scala_version == 'kind-projector'


def test_artifact_id_without_scala_version_when_scala_version_is_implicit_and_artifact_id_has_underscores():
    name = JvmPackageName('org.spire-math', 'kind_projector_2.10')
    assert name.artifact_id_without_scala_version == 'kind_projector'


def test_artifact_id_without_scala_version_when_scala_version_is_both_implicit_and_explicit():
    name = JvmPackageName('org.spire-math', 'kind-projector_2.10', '2.11')
    assert name.artifact_id_without_scala_version == 'kind-projector'


def test_artifact_id_without_scala_version_when_scala_version_is_none():
    name = JvmPackageName('org.spire-math', 'kind-projector')
    assert name.artifact_id_without_scala_version == 'kind-projector'


def test_get_scala_version_when_scala_version_is_explicit():
    name = JvmPackageName('org.spire-math', 'kind-projector', '2.10')
    assert name.scala_version == '2.10'


def test_get_scala_version_when_scala_version_is_implicit():
    name = JvmPackageName('org.spire-math', 'kind-projector_2.10')
    assert name.scala_version == '2.10'


def test_get_scala_version_when_scala_version_is_both_implicit_and_explicit():
    name = JvmPackageName('org.spire-math', 'kind-projector_2.10', '2.11')
    assert name.scala_version == '2.10'


def test_get_scala_version_when_scala_version_is_none():
    name = JvmPackageName('org.spire-math', 'kind-projector')
    assert name.scala_version is None


def test_equal_with_implicit_scala_version():
    a = JvmPackageName('org.spire-math', 'kind-projector_2.10')
    b = JvmPackageName('org.spire-math', 'kind-projector_2.10')
    assert a == b
    assert not a != b


def test_equal_with_explicit_scala_version():
    a = JvmPackageName('org.spire-math', 'kind-projector', '2.10')
    b = JvmPackageName('org.spire-math', 'kind-projector', '2.10')
    assert a == b
    assert not a != b


def test_equal_between_implicit_and_explicit_scala_versions():
    a = JvmPackageName('org.spire-math', 'kind-projector', '2.10')
    b = JvmPackageName('org.spire-math', 'kind-projector_2.10')
    assert a == b
    assert b == a
    assert not a != b
    assert not b != a


def test_not_equal_if_group_ids_are_different():
    a = JvmPackageName('foo', 'kind-projector', '2.10')
    b = JvmPackageName('bar', 'kind-projector', '2.10')
    assert a != b
    assert not a == b


def test_not_equal_if_artifact_ids_are_different():
    a = JvmPackageName('org.spire-math', 'foo', '2.10')
    b = JvmPackageName('org.spire-math', 'bar', '2.10')
    assert a != b
    assert not a == b


def test_not_equal_if_scala_versions_are_different():
    a = JvmPackageName('org.spire-math', 'kind-projector', '2.10')
    b = JvmPackageName('org.spire-math', 'kind-projector', '2.11')
    assert a != b
    assert not a == b


def test_str_with_explicit_scala_version():
    name = JvmPackageName('org.spire-math', 'kind-projector', '2.10')
    assert str(name) == 'org.spire-math:kind-projector_2.10'
    assert repr(name) == 'org.spire-math:kind-projector_2.10'


def test_str_with_implicit_scala_version():
    name = JvmPackageName('org.spire-math', 'kind-projector_2.10')
    assert str(name) == 'org.spire-math:kind-projector_2.10'
    assert repr(name) == 'org.spire-math:kind-projector_2.10'


def test_str_without_scala_version():
    name = JvmPackageName('org.spire-math', 'kind-projector')
    assert str(name) == 'org.spire-math:kind-projector'
    assert repr(name) == 'org.spire-math:kind-projector'
