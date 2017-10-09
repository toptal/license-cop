import pytest

from test import *
from app.platforms.jvm.package_name import JvmPackageName
from app.platforms.jvm.maven2_package_registry import Maven2PackageRegistry
from app.dependency import Dependency
from app.package_registry import PackageVersionNotFoundError


@pytest.fixture
def registry():
    return Maven2PackageRegistry(http_compression=False)


@VCR.use_cassette('maven2_package_registry_fetch_version.yaml')
def test_fetch_version(registry):
    name = JvmPackageName('org.spire-math', 'kind-projector_2.10')
    version = registry.fetch_version(name, '0.8.2')
    assert version.name == name
    assert version.number == '0.8.2'
    assert version.licenses == ['MIT']
    assert set(version.runtime_dependencies) == set([
        Dependency.runtime(JvmPackageName('org.scala-lang', 'scala-compiler')),
        Dependency.runtime(JvmPackageName('org.scala-lang', 'scala-library'))
    ])
    assert version.development_dependencies == []


@VCR.use_cassette('maven2_package_registry_fetch_version_appending_scala_version.yaml')
def test_fetch_version_appending_scala_version(registry):
    name = JvmPackageName('org.spire-math', 'kind-projector')
    version = registry.fetch_version(name, '0.8.2')
    assert version.name == name
    assert version.number == '0.8.2'
    assert version.licenses == ['MIT']
    assert set(version.runtime_dependencies) == set([
        Dependency.runtime(JvmPackageName('org.scala-lang', 'scala-compiler')),
        Dependency.runtime(JvmPackageName('org.scala-lang', 'scala-library'))
    ])
    assert version.development_dependencies == []


@VCR.use_cassette('maven2_package_registry_fetch_latest_version.yaml')
def test_fetch_latest_version(registry):
    name = JvmPackageName('org.spire-math', 'kind-projector_2.10')
    version = registry.fetch_latest_version(name)
    assert version.name == name
    assert version.number == '0.9.4'
    assert version.licenses == ['MIT']
    assert set(version.runtime_dependencies) == set([
        Dependency.runtime(JvmPackageName('org.scala-lang', 'scala-compiler')),
        Dependency.runtime(JvmPackageName('org.scala-lang', 'scala-library')),
        Dependency.runtime(JvmPackageName('org.scalamacros', 'quasiquotes_2.10'))
    ])
    assert set(version.development_dependencies) == set([
        Dependency.development(JvmPackageName('com.novocode', 'junit-interface')),
        Dependency.development(JvmPackageName('org.ensime', 'pcplod_2.10'))
    ])


@VCR.use_cassette('maven2_package_registry_fetch_latest_version_appending_scala_version.yaml')
def test_fetch_latest_version_appending_scala_version(registry):
    name = JvmPackageName('org.spire-math', 'kind-projector')
    version = registry.fetch_version(name, '0.8.2')
    assert version.name == name
    assert version.number == '0.8.2'
    assert version.licenses == ['MIT']
    assert set(version.runtime_dependencies) == set([
        Dependency.runtime(JvmPackageName('org.scala-lang', 'scala-compiler')),
        Dependency.runtime(JvmPackageName('org.scala-lang', 'scala-library'))
    ])
    assert version.development_dependencies == []


@pytest.mark.skip
@VCR.use_cassette('maven2_package_registry_fetch_version_group_id_not_found.yaml')
def test_fetch_version_group_id_not_found(registry):
    name = JvmPackageName('com.example.foobar', 'foobar')
    with pytest.raises(PackageVersionNotFoundError) as e:
        registry.fetch_version(name, '3.2.1')
    assert str(e.value) == (
        'Could not find package version com.example.foobar:foobar:3.2.1. '
        '404 Client Error: Not Found for url: '
        'https://repo.maven.apache.org/maven2/com/example/foobar/foobar/3.2.1/foobar-3.2.1.pom'
    )


@pytest.mark.skip
@VCR.use_cassette('maven2_package_registry_fetch_version_artifact_id_not_found.yaml')
def test_fetch_version_artifact_id_not_found(registry):
    name = JvmPackageName('org.scala-lang', 'foobar')
    with pytest.raises(PackageVersionNotFoundError) as e:
        registry.fetch_version(name, '3.2.1')
    assert str(e.value) == (
        'Could not find package version org.scala-lang:foobar:3.2.1. '
        '404 Client Error: Not Found for url: '
        'https://repo.maven.apache.org/maven2/org/scala-lang/foobar/3.2.1/foobar-3.2.1.pom'
    )


@pytest.mark.skip
@VCR.use_cassette('maven2_package_registry_fetch_version_number_not_found.yaml')
def test_fetch_version_number_not_found(registry):
    name = JvmPackageName('org.scala-lang', 'scala-compiler')
    with pytest.raises(PackageVersionNotFoundError) as e:
        registry.fetch_version(name, '666')
    assert str(e.value) == (
        'Could not find package version org.scala-lang:scala-compiler:666. '
        '404 Client Error: Not Found for url: '
        'https://repo.maven.apache.org/maven2/org/scala-lang/scala-compiler/666/scala-compiler-666.pom'
    )


@pytest.mark.skip
@VCR.use_cassette('maven2_package_registry_fetch_latest_version_group_id_not_found.yaml')
def test_fetch_latest_version_group_id_not_found(registry):
    name = JvmPackageName('com.example.foobar', 'foobar')
    with pytest.raises(PackageVersionNotFoundError) as e:
        registry.fetch_latest_version(name)
    assert str(e.value) == (
        'Could not find package version com.example.foobar:foobar:latest. '
        '404 Client Error: Not Found for url: '
        'https://repo.maven.apache.org/maven2/com/example/foobar/foobar/maven-metadata.xml'
    )


@pytest.mark.skip
@VCR.use_cassette('maven2_package_registry_fetch_latest_version_artifact_id_not_found.yaml')
def test_fetch_latest_version_artifact_id_not_found(registry):
    name = JvmPackageName('org.scala-lang', 'foobar')
    with pytest.raises(PackageVersionNotFoundError) as e:
        registry.fetch_latest_version(name)
    assert str(e.value) == (
        'Could not find package version org.scala-lang:foobar:latest. '
        '404 Client Error: Not Found for url: '
        'https://repo.maven.apache.org/maven2/org/scala-lang/foobar/maven-metadata.xml'
    )
