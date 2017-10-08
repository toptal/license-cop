import re

from app.dependency import *
from app.repository_matcher import *
from app.package_descriptor import *
from app.platforms.jvm.package_name import *


DEPENDENCY_REGEX = re.compile(
    r'"(?P<group>[\w\.\-]+)"\s*%%?\s*'    # group id
    r'"(?P<artifact>[\w\.\-]+)"\s*%\s*'   # artifact id
    r'"(?P<number>[\w\.\-]+)"'            # version number
    r'(\s*%\s*(?P<test>"?([Ttest])"?))?'  # optional test tag
)


def parse_scala_dependency(line):
    m = DEPENDENCY_REGEX.search(line)
    if m:
        name = JvmPackageName(m.group('group'), m.group('artifact'))
        kind = DependencyKind.DEVELOPMENT if m.group('test') else DependencyKind.RUNTIME
        return Dependency(name, kind)


class ScalaRepositoryMatcher(RepositoryMatcher):

    def __init__(self):
        super().__init__(['build.sbt'])

    def _fetch_package_descriptor(self, repository, match):
        assert len(match.nodes) == 1
        build_sbt = match.nodes[0]

        paths = []
        paths.append(build_sbt.path)
        paths.extend(self.__paths_from_project_folder(build_sbt))
        dependencies = self.__extract_dependencies(repository, paths)

        return PackageDescriptor(
            platform='Scala',
            repository=repository,
            paths=match.paths,
            runtime_dependencies=list(filter(lambda i: i.is_runtime, dependencies)),
            development_dependencies=list(filter(lambda i: i.is_development, dependencies))
        )

    def __paths_from_project_folder(self, build_sbt):
        results = build_sbt.search_siblings('project')
        if results and results[0].is_tree:
            project_folder = results[0]
            scala_files = []
            scala_files.extend(project_folder.deep_search('*.sbt'))
            scala_files.extend(project_folder.deep_search('*.scala'))
            return map(lambda i: i.path, scala_files)
        return []

    def __extract_dependencies(self, repository, paths):
        dependencies = set()
        for line in self.__all_non_blank_lines(repository, paths):
            d = parse_scala_dependency(line)
            if d:
                dependencies.add(d)
        return dependencies

    def __all_non_blank_lines(self, repository, paths):
        for path in paths:
            data = repository.read_text_file(path)
            for line in data.splitlines():
                line = line.strip()
                if line:
                    yield line
