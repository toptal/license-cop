import pytest

from app.platforms.jvm.package_name import JvmPackageName


def test_get_group_id():
    name = JvmPackageName('org.spire-math', 'kind-projector_2.10.6')
    assert name.group_id == 'org.spire-math'


def test_get_group_path():
    name = JvmPackageName('org.spire-math', 'kind-projector_2.10.6')
    assert name.group_path == 'org/spire-math'


def test_get_artifact_id_when_it_was_given_without_scala_version():
    name = JvmPackageName('org.spire-math', 'kind-projector')
    assert name.artifact_id == 'kind-projector'


def test_get_artifact_id_when_it_was_given_with_scala_version():
    name = JvmPackageName('org.spire-math', 'kind-projector_2.10.6')
    assert name.artifact_id == 'kind-projector'


def test_get_scala_version_when_it_was_given_explicitly():
    name = JvmPackageName('org.spire-math', 'kind-projector', '2.10.6')
    assert name.scala_version == '2.10.6'


def test_get_scala_version_when_it_was_given_implicitly_in_the_artifact_id():
    name = JvmPackageName('org.spire-math', 'kind-projector_2.10.6')
    assert name.scala_version == '2.10.6'


def test_get_scala_version_when_it_was_not_given():
    name = JvmPackageName('org.spire-math', 'kind-projector')
    assert name.scala_version is None


def test_get_scala_version_without_patch_given_only_major_and_minor_parts():
    name = JvmPackageName('org.spire-math', 'kind-projector', '2.10')
    assert name.scala_version_without_patch == '2.10'


def test_get_scala_version_without_patch_given_major_minor_and_patch_parts():
    name = JvmPackageName('org.spire-math', 'kind-projector', '2.10.5')
    assert name.scala_version_without_patch == '2.10'


def test_get_scala_version_without_patch_given_major_minor_patch_and_pre_release_parts():
    name = JvmPackageName('org.spire-math', 'kind-projector', '2.10.5-RC2')
    assert name.scala_version_without_patch == '2.10'


def test_get_artifact_id_variations_when_there_is_no_scala_version():
    name = JvmPackageName('org.spire-math', 'kind-projector')
    assert name.artifact_id_variations == ('kind-projector',)


def test_get_artifact_id_variations_when_there_is_scala_version():
    name = JvmPackageName('org.spire-math', 'kind-projector', '2.10.5-RC2')
    assert name.artifact_id_variations == (
        'kind-projector_2.10.5-RC2',
        'kind-projector_2.10',
        'kind-projector'
    )


def test_equality_when_both_instances_have_scala_versions_implicit_in_artifact_id():
    a = JvmPackageName('org.spire-math', 'kind-projector_2.10.6')
    b = JvmPackageName('org.spire-math', 'kind-projector_2.10.6')
    assert a == b
    assert not a != b


def test_equality_when_both_instances_have_explicit_scala_versions():
    a = JvmPackageName('org.spire-math', 'kind-projector', '2.10.6')
    b = JvmPackageName('org.spire-math', 'kind-projector', '2.10.6')
    assert a == b
    assert not a != b


def test_equality_between_instances_with_implicit_and_explicit_scala_versions():
    a = JvmPackageName('org.spire-math', 'kind-projector', '2.10.6')
    b = JvmPackageName('org.spire-math', 'kind-projector_2.10.6')
    assert a == b
    assert b == a
    assert not a != b
    assert not b != a


def test_unequality_between_instances_with_different_group_ids():
    a = JvmPackageName('foo', 'kind-projector', '2.10.6')
    b = JvmPackageName('bar', 'kind-projector', '2.10.6')
    assert a != b
    assert not a == b


def test_unequality_between_instances_with_different_artifact_ids():
    a = JvmPackageName('org.spire-math', 'foo', '2.10.6')
    b = JvmPackageName('org.spire-math', 'bar', '2.10.6')
    assert a != b
    assert not a == b


def test_unequality_between_instances_with_different_scala_versions():
    a = JvmPackageName('org.spire-math', 'kind-projector', '2.10.6')
    b = JvmPackageName('org.spire-math', 'kind-projector', '2.11')
    assert a != b
    assert not a == b


def test_string_representation_given_explicit_scala_version():
    name = JvmPackageName('org.spire-math', 'kind-projector', '2.10.6')
    assert str(name) == 'org.spire-math:kind-projector_2.10.6'
    assert repr(name) == 'org.spire-math:kind-projector_2.10.6'


def test_string_representation_given_scala_version_implicit_in_artifact_id():
    name = JvmPackageName('org.spire-math', 'kind-projector_2.10.6')
    assert str(name) == 'org.spire-math:kind-projector_2.10.6'
    assert repr(name) == 'org.spire-math:kind-projector_2.10.6'


def test_string_representation_given_no_scala_version():
    name = JvmPackageName('org.spire-math', 'kind-projector')
    assert str(name) == 'org.spire-math:kind-projector'
    assert repr(name) == 'org.spire-math:kind-projector'
