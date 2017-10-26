import pytest

from app.platforms.jvm.maven_pom import MavenPom
from app.platforms.jvm.maven_dependency import MavenDependency
from app.dependency import Dependency, DependencyKind


@pytest.fixture
def simple_pom():
    return MavenPom(
        group_id='com.example',
        artifact_id='foobar',
        version='1.2.3',
        parent=None,
        properties={}
    )


@pytest.fixture
def complex_pom(parent_pom):
    return MavenPom(
        group_id='com.example',
        artifact_id='foobar',
        version='1.2.3',
        parent=parent_pom,
        properties={
            'foo.bar': 'FooBar',
            'Hello-World': 'hello-world'
        }
    )


@pytest.fixture
def parent_pom(grandparent_pom):
    return MavenPom(
        group_id='com.example',
        artifact_id='foobar-parent',
        version='1.2.3',
        parent=grandparent_pom,
        properties={
            'hiThere': 'hi_there',
            'omg': 'oh-my-god'
        }
    )


@pytest.fixture
def grandparent_pom():
    return MavenPom(
        group_id='com.example',
        artifact_id='foobar-grandparent',
        version='1.2.3',
        parent=None,
        properties={
            'yo': 'yo'
        }
    )


def test_to_runtime_dependency_given_none_scope(simple_pom):
    dependency = MavenDependency('com.example', 'foobar', None).to_dependency(simple_pom)
    assert dependency.is_runtime


def test_to_runtime_dependency_given_empty_scope(simple_pom):
    dependency = MavenDependency('com.example', 'foobar', '').to_dependency(simple_pom)
    assert dependency.is_runtime


def test_to_runtime_dependency_given_non_test_scope(simple_pom):
    dependency = MavenDependency('com.example', 'foobar', 'compile').to_dependency(simple_pom)
    assert dependency.is_runtime


def test_to_development_dependency_given_test_scope(simple_pom):
    dependency = MavenDependency('com.example', 'foobar', 'test').to_dependency(simple_pom)
    assert dependency.is_development


def test_to_dependency_without_interpolation(simple_pom):
    dependency = MavenDependency('com.example', 'foobar', None).to_dependency(simple_pom)
    assert dependency.name.group_id == 'com.example'
    assert dependency.name.artifact_id == 'foobar'


def test_to_dependency_with_interpolation_from_immediate_properties(complex_pom):
    group_id = 'com.${foo.bar}'
    artifact_id = '${Hello-World}_2.11'
    dependency = MavenDependency(group_id, artifact_id).to_dependency(complex_pom)
    assert dependency.name.group_id == 'com.FooBar'
    assert dependency.name.artifact_id == 'hello-world'


def test_to_dependency_with_interpolation_from_nested_properties(complex_pom):
    group_id = '${foo.bar}-${omg}'
    artifact_id = '${Hello-World}-${hiThere}#${yo}'
    dependency = MavenDependency(group_id, artifact_id).to_dependency(complex_pom)
    assert dependency.name.group_id == 'FooBar-oh-my-god'
    assert dependency.name.artifact_id == 'hello-world-hi_there#yo'


def test_to_dependency_with_interpolation_from_builtin_properties(complex_pom):
    group_id = '${project.groupId}-foobar'
    artifact_id = '${project.artifactId}-${project.version}-foobar'
    dependency = MavenDependency(group_id, artifact_id).to_dependency(complex_pom)
    assert dependency.name.group_id == 'com.example-foobar'
    assert dependency.name.artifact_id == 'foobar-1.2.3-foobar'
