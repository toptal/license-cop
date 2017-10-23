import pytest

from test import *
from app.platforms.scala.repository_matcher import *
from app.platforms.jvm.package_name import *
from app.github.repository import *


def dependency_line(expression):
    return f'libraryDependencies ++=  Seq({expression}, // this is a "comment"'


def test_does_not_parse_malformed_scala_dependency():
    line = dependency_line('"org.scala-tools" %%% "scala-stm" % "0.3"')
    assert parse_scala_dependency(line) is None


def test_parse_runtime_scala_dependency_without_scala_version():
    line = dependency_line('"org.scala-tools" %% "scala-stm" % "0.3"')
    dependency = parse_scala_dependency(line)
    assert str(dependency.name) == 'org.scala-tools:scala-stm'
    assert dependency.is_runtime


def test_parse_runtime_scala_dependency_with_scala_version():
    line = dependency_line('"org.scala-tools" % "scala-stm_2.11.1" % "0.3"')
    dependency = parse_scala_dependency(line)
    assert str(dependency.name) == 'org.scala-tools:scala-stm_2.11.1'
    assert dependency.is_runtime


def test_parse_development_scala_dependency_with_test_constant():
    line = dependency_line('"org.scala-tools" %% "scala-stm" % "0.3" % Test')
    dependency = parse_scala_dependency(line)
    assert str(dependency.name) == 'org.scala-tools:scala-stm'
    assert dependency.is_development


def test_parse_development_scala_dependency_with_lowercase_test_string():
    line = dependency_line('"org.scala-tools" %% "scala-stm" % "0.3" % "test"')
    dependency = parse_scala_dependency(line)
    assert str(dependency.name) == 'org.scala-tools:scala-stm'
    assert dependency.is_development


def test_parse_development_scala_dependency_with_capitalized_test_string():
    line = dependency_line('"org.scala-tools" %% "scala-stm" % "0.3" % "Test"')
    dependency = parse_scala_dependency(line)
    assert str(dependency.name) == 'org.scala-tools:scala-stm'
    assert dependency.is_development


def test_parse_development_scala_dependency_with_any_test_configuration():
    line = dependency_line('"org.scala-tools" % "scala-stm" % "0.3" % "compile->compile;test->test"')
    dependency = parse_scala_dependency(line)
    assert str(dependency.name) == 'org.scala-tools:scala-stm'
    assert dependency.is_development


def test_parse_runtime_scala_dependency_without_scala_version_but_single_percent():
    line = dependency_line('"com.typesafe.play" % "sbt-plugin" % "2.3.9"')
    dependency = parse_scala_dependency(line)
    assert str(dependency.name) == 'com.typesafe.play:sbt-plugin'
    assert dependency.is_runtime


def test_parse_scala_dependency_with_snapshot_scala_version():
    line = dependency_line('"org.scala-tools" % "scala-stm_2.12.0-SNAPSHOT" % "0.3" % Test')
    dependency = parse_scala_dependency(line)
    assert str(dependency.name) == 'org.scala-tools:scala-stm_2.12.0-SNAPSHOT'


def test_parse_scala_dependency_with_scala_version_with_underscore_in_artifact_id():
    line = dependency_line('"java_cup" % "java_cup_2.11.0" % "0.9e"')
    dependency = parse_scala_dependency(line)
    assert str(dependency.name) == 'java_cup:java_cup_2.11.0'


def test_parse_scala_dependency_without_scala_version_with_underscore_in_artifact_id():
    line = dependency_line('"java_cup" % "java_cup" % "0.9e"')
    dependency = parse_scala_dependency(line)
    assert str(dependency.name) == 'java_cup:java_cup'


def test_parse_scala_dependency_with_snapshot_version():
    line = dependency_line('"com.typesafe.play" %% "sbt-plugin" % "2.3.9-SNAPSHOT" % Test')
    dependency = parse_scala_dependency(line)
    assert str(dependency.name) == 'com.typesafe.play:sbt-plugin'


def test_parse_scala_dependency_with_version_from_variable():
    line = dependency_line('"com.typesafe.play" %% "sbt-plugin" % fooBar.version % Test')
    dependency = parse_scala_dependency(line)
    assert str(dependency.name) == 'com.typesafe.play:sbt-plugin'


def scala_version_line(expression):
    return f'   {expression}, // foobar '


def test_parse_scala_version_with_colon_equal_assignment():
    line = scala_version_line('scalaVersion := "2.11.11"')
    assert parse_scala_version(line) == '2.11.11'


def test_parse_scala_version_with_equal_assignment():
    line = scala_version_line('scalaVersion = "2.11.11"')
    assert parse_scala_version(line) == '2.11.11'


def test_parse_scala_version_with_snapshot_version():
    line = scala_version_line('scalaVersion = "2.11.11-SNAPSHOT"')
    assert parse_scala_version(line) == '2.11.11-SNAPSHOT'


def test_does_not_parse_scala_version_assigned_from_variable():
    line = scala_version_line('scalaVersion = foobar')
    assert parse_scala_version(line) is None


def test_does_not_parse_malformed_scala_version():
    line = scala_version_line('scalaVersion == "2.11.1"')
    assert parse_scala_version(line) is None


def test_does_not_parse_random_assignment():
    line = scala_version_line('foobar = "2.11.1"')
    assert parse_scala_version(line) is None


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


def runtime_dependency(group_id, artifact_id, scala_version):
    return Dependency.runtime(JvmPackageName(group_id, artifact_id, scala_version))


def development_dependency(group_id, artifact_id, scala_version):
    return Dependency.development(JvmPackageName(group_id, artifact_id, scala_version))


@VCR.use_cassette('scala_repository_matcher_manifest_from_build_sbt_with_project_folder.yaml')
def test_manifest_from_build_sbt_with_project_folder(matcher, scala_repository):
    match = matcher.match(scala_repository)
    manifest = match.manifest_at('framework/build.sbt')

    assert manifest.platform == 'Scala'
    assert manifest.repository == scala_repository
    assert manifest.paths == ['framework/build.sbt']

    scala_version = '2.12.3'

    assert set(manifest.development_dependencies) == set([
        development_dependency('com.github.ben-manes.caffeine', 'jcache', scala_version),
        development_dependency('org.hibernate', 'hibernate-entitymanager', scala_version),
        development_dependency('org.scalacheck', 'scalacheck', scala_version),
        development_dependency('org.specs2', 'specs2-scalacheck', scala_version)
    ])

    assert set(manifest.runtime_dependencies) == set([
        runtime_dependency('ch.qos.logback', 'logback-classic', scala_version),
        runtime_dependency('com.eed3si9n', 'sbt-buildinfo', scala_version),
        runtime_dependency('com.eed3si9n', 'sbt-doge', scala_version),
        runtime_dependency('com.google.code.findbugs', 'jsr305', scala_version),
        runtime_dependency('com.google.inject', 'guice', scala_version),
        runtime_dependency('com.google.inject.extensions', 'guice-assistedinject', scala_version),
        runtime_dependency('com.google.guava', 'guava', scala_version),
        runtime_dependency('com.googlecode.usc', 'jdbcdslog', scala_version),
        runtime_dependency('com.h2database', 'h2', scala_version),
        runtime_dependency('com.jolbox', 'bonecp', scala_version),
        runtime_dependency('com.lightbend.play', 'play-file-watch', scala_version),
        runtime_dependency('com.lightbend.sbt', 'sbt-javaagent', scala_version),
        runtime_dependency('com.novocode', 'junit-interface', scala_version),
        runtime_dependency('com.squareup.okhttp3', 'okhttp', scala_version),
        runtime_dependency('com.typesafe', 'config', scala_version),
        runtime_dependency('com.typesafe', 'sbt-mima-plugin', scala_version),
        runtime_dependency('com.typesafe.akka', 'akka-stream', scala_version),
        runtime_dependency('com.typesafe.netty', 'netty-reactive-streams-http', scala_version),
        runtime_dependency('com.typesafe.play', 'interplay', scala_version),
        runtime_dependency('com.typesafe.play', 'play-ahc-ws-standalone', scala_version),
        runtime_dependency('com.typesafe.play', 'play-doc', scala_version),
        runtime_dependency('com.typesafe.play', 'play-json', scala_version),
        runtime_dependency('com.typesafe.play', 'play-ws-standalone', scala_version),
        runtime_dependency('com.typesafe.play', 'play-ws-standalone-json', scala_version),
        runtime_dependency('com.typesafe.play', 'play-ws-standalone-xml', scala_version),
        runtime_dependency('com.typesafe.play', 'shaded-asynchttpclient', scala_version),
        runtime_dependency('com.typesafe.play', 'shaded-oauth', scala_version),
        runtime_dependency('com.typesafe.sbt', 'sbt-js-engine', scala_version),
        runtime_dependency('com.typesafe.sbt', 'sbt-native-packager', scala_version),
        runtime_dependency('com.typesafe.sbt', 'sbt-twirl', scala_version),
        runtime_dependency('com.typesafe.sbt', 'sbt-web', scala_version),
        runtime_dependency('com.zaxxer', 'HikariCP', scala_version),
        runtime_dependency('commons-codec', 'commons-codec', scala_version),
        runtime_dependency('commons-io', 'commons-io', scala_version),
        runtime_dependency('de.heikoseeberger', 'sbt-header', scala_version),
        runtime_dependency('io.jsonwebtoken', 'jjwt', scala_version),
        runtime_dependency('io.netty', 'netty-transport-native-epoll', scala_version),
        runtime_dependency('joda-time', 'joda-time', scala_version),
        runtime_dependency('javax.transaction', 'jta', scala_version),
        runtime_dependency('javax.inject', 'javax.inject', scala_version),
        runtime_dependency('junit', 'junit', scala_version),
        runtime_dependency('net.jodah', 'typetools', scala_version),
        runtime_dependency('org.apache.commons', 'commons-lang3', scala_version),
        runtime_dependency('org.apache.derby', 'derby', scala_version),
        runtime_dependency('org.easytesting', 'fest-assert', scala_version),
        runtime_dependency('org.ehcache', 'jcache', scala_version),
        runtime_dependency('org.eu.acolyte', 'jdbc-driver', scala_version),
        runtime_dependency('org.fluentlenium', 'fluentlenium-core', scala_version),
        runtime_dependency('org.hibernate', 'hibernate-validator', scala_version),
        runtime_dependency('org.hibernate.javax.persistence', 'hibernate-jpa-2.1-api', scala_version),
        runtime_dependency('org.joda', 'joda-convert', scala_version),
        runtime_dependency('org.mockito', 'mockito-all', scala_version),
        runtime_dependency('org.mortbay.jetty.alpn', 'jetty-alpn-agent', scala_version),
        runtime_dependency('org.reactivestreams', 'reactive-streams', scala_version),
        runtime_dependency('org.reflections', 'reflections', scala_version),
        runtime_dependency('org.scala-lang', 'scala-reflect', scala_version),
        runtime_dependency('org.scala-lang.modules', 'scala-java8-compat', scala_version),
        runtime_dependency('org.scala-lang.modules', 'scala-parser-combinators', scala_version),
        runtime_dependency('org.scala-sbt', 'io', scala_version),
        runtime_dependency('org.scala-sbt', 'scripted-plugin', scala_version),
        runtime_dependency('org.scalariform', 'sbt-scalariform', scala_version),
        runtime_dependency('org.seleniumhq.selenium', 'htmlunit-driver', scala_version),
        runtime_dependency('org.seleniumhq.selenium', 'selenium-api', scala_version),
        runtime_dependency('org.seleniumhq.selenium', 'selenium-firefox-driver', scala_version),
        runtime_dependency('org.seleniumhq.selenium', 'selenium-support', scala_version),
        runtime_dependency('org.slf4j', 'slf4j-simple', scala_version),
        runtime_dependency('org.specs2', 'specs2-matcher-extra', scala_version),
        runtime_dependency('org.springframework', 'spring-beans', scala_version),
        runtime_dependency('org.springframework', 'spring-core', scala_version),
        runtime_dependency('org.springframework', 'spring-context', scala_version),
        runtime_dependency('org.webjars', 'jquery', scala_version),
        runtime_dependency('org.webjars', 'prettify', scala_version),
        runtime_dependency('org.webjars', 'webjars-locator-core', scala_version),
        runtime_dependency('tyrex', 'tyrex', scala_version),
        runtime_dependency('javax.cache', 'cache-api', scala_version),
        runtime_dependency('net.sf.ehcache', 'ehcache', scala_version),
        runtime_dependency('pl.project13.scala', 'sbt-jmh', scala_version)
    ])
