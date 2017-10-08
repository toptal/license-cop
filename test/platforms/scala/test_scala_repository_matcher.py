import pytest

from test import *
from app.platforms.scala.repository_matcher import *
from app.platforms.jvm.package_name import *
from app.github.repository import *


def build_line(expression):
    return 'libraryDependencies ++={0}, // this is a "comment"'.format(expression)


def test_does_not_parse_malformed_scala_dependency_without_scala_version():
    line = build_line('"org.scala-tools" %%% "scala-stm" % "0.3"')
    assert parse_scala_dependency(line) is None


def test_parse_runtime_scala_dependency_without_scala_version():
    line = build_line('"org.scala-tools" %% "scala-stm" % "0.3"')
    dependency = parse_scala_dependency(line)
    assert str(dependency.name) == 'org.scala-tools:scala-stm'
    assert dependency.is_runtime


def test_parse_development_scala_dependency_without_scala_version_with_test_constant():
    line = build_line('"org.scala-tools" %% "scala-stm" % "0.3" % Test')
    dependency = parse_scala_dependency(line)
    assert str(dependency.name) == 'org.scala-tools:scala-stm'
    assert dependency.is_development


def test_parse_development_scala_dependency_without_scala_version_with_lowercase_test_string():
    line = build_line('"org.scala-tools" %% "scala-stm" % "0.3" % "test"')
    dependency = parse_scala_dependency(line)
    assert str(dependency.name) == 'org.scala-tools:scala-stm'
    assert dependency.is_development


def test_parse_development_scala_dependency_without_scala_version_with_capitalized_test_string():
    line = build_line('"org.scala-tools" %% "scala-stm" % "0.3" % "Test"')
    dependency = parse_scala_dependency(line)
    assert str(dependency.name) == 'org.scala-tools:scala-stm'
    assert dependency.is_development


def test_parse_runtime_scala_dependency_with_scala_version():
    line = build_line('"org.scala-tools" % "scala-stm_2.11.1" % "0.3"')
    dependency = parse_scala_dependency(line)
    assert str(dependency.name) == 'org.scala-tools:scala-stm_2.11.1'
    assert dependency.is_runtime


def test_parse_development_scala_dependency_with_scala_version_with_test_constant():
    line = build_line('"org.scala-tools" % "scala-stm_2.11.1" % "0.3" % Test')
    dependency = parse_scala_dependency(line)
    assert str(dependency.name) == 'org.scala-tools:scala-stm_2.11.1'
    assert dependency.is_development


def test_parse_development_scala_dependency_with_scala_version_with_lowercase_test_string():
    line = build_line('"org.scala-tools" % "scala-stm_2.11.1" % "0.3" % "test"')
    dependency = parse_scala_dependency(line)
    assert str(dependency.name) == 'org.scala-tools:scala-stm_2.11.1'
    assert dependency.is_development


def test_parse_development_scala_dependency_with_scala_version_with_capitalized_test_string():
    line = build_line('"org.scala-tools" % "scala-stm_2.11.1" % "0.3" % "Test"')
    dependency = parse_scala_dependency(line)
    assert str(dependency.name) == 'org.scala-tools:scala-stm_2.11.1'
    assert dependency.is_development


def test_parse_runtime_scala_dependency_without_scala_version_but_single_percent():
    line = build_line('"com.typesafe.play" % "sbt-plugin" % "2.3.9"')
    dependency = parse_scala_dependency(line)
    assert str(dependency.name) == 'com.typesafe.play:sbt-plugin'
    assert dependency.is_runtime


def test_parse_scala_dependency_with_snapshot_scala_version():
    line = build_line('"org.scala-tools" % "scala-stm_2.12.0-SNAPSHOT" % "0.3"')
    dependency = parse_scala_dependency(line)
    assert str(dependency.name) == 'org.scala-tools:scala-stm_2.12.0-SNAPSHOT'


def test_parse_scala_dependency_with_scala_version_with_underscore_in_artifact_id():
    line = build_line('"java_cup" % "java_cup_2.11.0" % "0.9e"')
    dependency = parse_scala_dependency(line)
    assert str(dependency.name) == 'java_cup:java_cup_2.11.0'


def test_parse_scala_dependency_without_scala_version_with_underscore_in_artifact_id():
    line = build_line('"java_cup" % "java_cup" % "0.9e"')
    dependency = parse_scala_dependency(line)
    assert str(dependency.name) == 'java_cup:java_cup'


def test_parse_scala_dependency_with_snapshot_version():
    line = build_line('"com.typesafe.play" %% "sbt-plugin" % "2.3.9-SNAPSHOT"')
    dependency = parse_scala_dependency(line)
    assert str(dependency.name) == 'com.typesafe.play:sbt-plugin'
    assert dependency.is_runtime


@pytest.fixture
def matcher():
    return ScalaRepositoryMatcher()


@pytest.fixture
def scala_repository():
    return GithubRepository.from_url(
        'https://github.com/playframework/playframework',
        http_compression=False
    )


@pytest.fixture
def ruby_repository():
    return GithubRepository.from_url(
        'https://github.com/rails/rails',
        http_compression=False
    )


@VCR.use_cassette('scala_repository_matcher_match_repository_with_build_sbt_file.yaml')
def test_match_repository_with_build_sbt_file(matcher, scala_repository):
    assert matcher.match(scala_repository) is not None


@VCR.use_cassette('scala_repository_matcher_mismatch_repository_without_build_sbt_file.yaml')
def test_mismatch_repository_without_sbt_file(matcher, ruby_repository):
    assert matcher.match(ruby_repository) is None


@VCR.use_cassette('scala_repository_matcher_package_descriptor_from_build_sbt_with_project_folder.yaml')
def test_package_descriptor_from_build_sbt_with_project_folder(matcher, scala_repository):
    match = matcher.match(scala_repository)
    descriptor = match.package_descriptor_at('framework/build.sbt')

    assert descriptor.platform == 'Scala'
    assert descriptor.repository == scala_repository
    assert descriptor.paths == ['framework/build.sbt']

    assert set(descriptor.development_dependencies) == set([
        Dependency.development(JvmPackageName('org.hibernate', 'hibernate-entitymanager')),
        Dependency.development(JvmPackageName('org.scalacheck', 'scalacheck'))
    ])

    assert set(descriptor.runtime_dependencies) == set([
        Dependency.runtime(JvmPackageName('ch.qos.logback', 'logback-classic')),
        Dependency.runtime(JvmPackageName('com.google.guava', 'guava')),
        Dependency.runtime(JvmPackageName('com.google.code.findbugs', 'jsr305')),
        Dependency.runtime(JvmPackageName('org.mockito', 'mockito-all')),
        Dependency.runtime(JvmPackageName('com.h2database', 'h2')),
        Dependency.runtime(JvmPackageName('org.apache.derby', 'derby')),
        Dependency.runtime(JvmPackageName('org.mortbay.jetty.alpn', 'jetty-alpn-agent')),
        Dependency.runtime(JvmPackageName('io.jsonwebtoken', 'jjwt')),
        Dependency.runtime(JvmPackageName('com.jolbox', 'bonecp')),
        Dependency.runtime(JvmPackageName('com.zaxxer', 'HikariCP')),
        Dependency.runtime(JvmPackageName('com.googlecode.usc', 'jdbcdslog')),
        Dependency.runtime(JvmPackageName('tyrex', 'tyrex')),
        Dependency.runtime(JvmPackageName('org.hibernate.javax.persistence', 'hibernate-jpa-2.1-api')),
        Dependency.runtime(JvmPackageName('org.scala-lang.modules', 'scala-java8-compat')),
        Dependency.runtime(JvmPackageName('org.scala-lang.modules', 'scala-parser-combinators')),
        Dependency.runtime(JvmPackageName('org.reflections', 'reflections')),
        Dependency.runtime(JvmPackageName('net.jodah', 'typetools')),
        Dependency.runtime(JvmPackageName('joda-time', 'joda-time')),
        Dependency.runtime(JvmPackageName('org.joda', 'joda-convert')),
        Dependency.runtime(JvmPackageName('com.eed3si9n', 'sbt-buildinfo')),
        Dependency.runtime(JvmPackageName('org.hibernate', 'hibernate-validator')),
        Dependency.runtime(JvmPackageName('com.novocode', 'junit-interface')),
        Dependency.runtime(JvmPackageName('junit', 'junit')),
        Dependency.runtime(JvmPackageName('org.easytesting', 'fest-assert')),
        Dependency.runtime(JvmPackageName('commons-codec', 'commons-codec')),
        Dependency.runtime(JvmPackageName('org.apache.commons', 'commons-lang3')),
        Dependency.runtime(JvmPackageName('javax.transaction', 'jta')),
        Dependency.runtime(JvmPackageName('javax.inject', 'javax.inject')),
        Dependency.runtime(JvmPackageName('com.typesafe.netty', 'netty-reactive-streams-http')),
        Dependency.runtime(JvmPackageName('com.squareup.okhttp3', 'okhttp')),
        Dependency.runtime(JvmPackageName('commons-io', 'commons-io')),
        Dependency.runtime(JvmPackageName('com.lightbend.play', 'play-file-watch')),
        Dependency.runtime(JvmPackageName('org.scala-sbt', 'io')),
        Dependency.runtime(JvmPackageName('com.typesafe', 'config')),
        Dependency.runtime(JvmPackageName('com.typesafe.sbt', 'sbt-web')),
        Dependency.runtime(JvmPackageName('com.typesafe.sbt', 'sbt-js-engine')),
        Dependency.runtime(JvmPackageName('org.webjars', 'jquery')),
        Dependency.runtime(JvmPackageName('org.webjars', 'prettify')),
        Dependency.runtime(JvmPackageName('org.reactivestreams', 'reactive-streams')),
        Dependency.runtime(JvmPackageName('org.fluentlenium', 'fluentlenium-core')),
        Dependency.runtime(JvmPackageName('org.seleniumhq.selenium', 'htmlunit-driver')),
        Dependency.runtime(JvmPackageName('javax.cache', 'cache-api')),
        Dependency.runtime(JvmPackageName('org.ehcache', 'jcache'))
    ])
