import re
from itertools import chain

from app.dependency import *
from app.repository_matcher import *
from app.manifest import *
from app.platforms.jvm.package_name import *


# We only support dependencies declared using the % operator tuple. Examples:
#
#    "org.hibernate" % "hibernate-validator" % "5.4.1.Final"
#    "org.hibernate" % "hibernate-entitymanager" % "5.2.11.Final" % "test"
#
# We do not support complex constructs, such as:
#
#    val slf4jVersion = "1.7.25"
#    val slf4j = Seq("slf4j-api", "jul-to-slf4j", "jcl-over-slf4j")
#                  .map("org.slf4j" % _ % slf4jVersion)
#
# To interpret that it would be necessary to build a Scala-like compiler.
#
# We're not concerned about version numbers for now. However, in case
# we want to extract them, we must parse them in the format:
#
#     "org.codehaus.jackson" % "jackson-core-asl" % "1.9.13"
#
# It's also very common to declare a shared version number in a
# variable, like this:
#
#    val http4sVersion = "0.14.2"
#
#    val http4s = Seq(
#      "org.http4s" %% "http4s-dsl" % http4sVersion,
#      "org.http4s" %% "http4s-jetty" % http4sVersion,
#      "org.http4s" %% "http4s-argonaut" % http4sVersion,
#      "org.http4s" %% "http4s-blaze-client" % http4sVersion
#    )
#
# So we would have to implement a two-way parse that first would parse
# variable assignments, like this:
#
#   val fooBar = "0.14.2"
#   val fooBar := "0.14.2"
#   var fooBar = "0.14.2"
#   var fooBar := "0.14.2"
#
# We would store these variables inside a dictionary. Then, whenever a
# variable reference was found inside a dependency declaration, we
# would substitute it with values from the dictionary.
DEPENDENCY_REGEX = re.compile(
    r'"(?P<group>[\w\.\-]+)"\s*%%?'
    r'\s*"(?P<artifact>[\w\.\-]+)"\s*%'
    r'\s*"?(?P<number>\S+)"?\s*'
    r'(%\s*(?P<configuration>\S+))?'
)

TEST_CONFIGURATION_REGEX = re.compile(r'[Tt]est')

SCALA_VERSION_REGEX = re.compile(r'scalaVersion\s:?=\s*"(\S+)"')


def __dependency_kind_from(configuration):
    if configuration:
        if TEST_CONFIGURATION_REGEX.search(configuration):
            return DependencyKind.DEVELOPMENT
    return DependencyKind.RUNTIME


def parse_scala_dependency(line, scala_version=None):
    m = DEPENDENCY_REGEX.search(line)
    if m:
        name = JvmPackageName(m.group('group'), m.group('artifact'), scala_version)
        kind = __dependency_kind_from(m.group('configuration'))
        return Dependency(name, kind)


def parse_scala_version(line):
    m = SCALA_VERSION_REGEX.search(line)
    if m:
        return m.group(1)


class ScalaRepositoryMatcher(RepositoryMatcher):

    def __init__(self):
        super().__init__(['build.sbt'])

    def _fetch_manifest(self, repository, match):
        assert len(match.nodes) == 1
        build_sbt = match.nodes[0]

        paths = [build_sbt.path] + self.__paths_from_project_folder(build_sbt)
        dependencies = self.__parse_scala_files(repository, paths)

        return Manifest(
            platform='Scala',
            repository=repository,
            paths=match.paths,
            runtime_dependencies=[i for i in dependencies if i.is_runtime],
            development_dependencies=[i for i in dependencies if i.is_development]
        )

    def __paths_from_project_folder(self, build_sbt):
        scala_files = []
        project_folder = build_sbt.parent.navigate('project')
        if project_folder and project_folder.is_tree:
            scala_files.extend(project_folder.deep_search('*.sbt'))
            scala_files.extend(project_folder.deep_search('*.scala'))
        return [i.path for i in scala_files]

    def __parse_scala_files(self, repository, paths):
        lines = self.__all_lines(repository, paths)
        scala_version = self.__find_scala_version(lines)
        return self.__extract_dependencies(lines, scala_version)

    def __find_scala_version(self, lines):
        for line in lines:
            s = parse_scala_version(line)
            if s:
                return s

    def __extract_dependencies(self, lines, scala_version):
        dependencies = set()
        for line in lines:
            d = parse_scala_dependency(line, scala_version)
            if d:
                dependencies.add(d)
        return dependencies

    def __all_lines(self, repository, paths):
        text_files = (repository.read_text_file(i) for i in paths)
        return list(chain.from_iterable(i.splitlines() for i in text_files))
