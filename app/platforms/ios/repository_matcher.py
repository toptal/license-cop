import re

from app.dependency import *
from app.repository_matcher import *
from app.package_descriptor import *


class IosRepositoryMatcher(RepositoryMatcher):

    def __init__(self):
        super().__init__([PackageDescriptorPattern.one_file('podfile', 'Podfile')])

    def _fetch_package_descriptor(self, repository, pattern_match):
        assert len(pattern_match.paths) == 1
        podfile = pattern_match.paths[0]

        data = repository.read_text_file(podfile)

        dependencies = []

        for line in data.splitlines():
            name = self.__parse_line(line)
            if name:
                dependency = self.__build_dependency(name)
                dependencies.append(dependency)

        return PackageDescriptor(
            platform='iOS',
            repository=repository,
            paths=[podfile],
            runtime_dependencies=dependencies,
            development_dependencies=[]  # TODO
        )

    def __parse_line(self, line):
        m = re.match(r"^\s*pod\s+['\"]([\w\-]+)[\/'\"]", line)
        return m.group(1) if m else None

    def __build_dependency(self, name):
        return Dependency.runtime(name)
