import re

from app.dependency import *
from app.repository_matcher import *
from app.package_descriptor import *


class ElixirRepositoryMatcher(RepositoryMatcher):

    def __init__(self):
        super().__init__([PackageDescriptorPattern.one_file('mix', 'mix.exs')])

    def _fetch_package_descriptor(self, repository, pattern_match):
        assert len(pattern_match.paths) == 1
        mixfile = pattern_match.paths[0]

        runtime_dependencies = []
        development_dependencies = []

        data = repository.read_text_file(mixfile)
        for dep in self.__each_dep(data):
            name, version, *options = [s.strip() for s in dep.split(',', 2)]
            package_name = name[1:]

            if options and ':dev' in options[0]:
                development_dependencies.append(Dependency.development(package_name))
            else:
                runtime_dependencies.append(Dependency.runtime(package_name))

        return PackageDescriptor(
            platform='Elixir',
            repository=repository,
            paths=[mixfile],
            runtime_dependencies=runtime_dependencies,
            development_dependencies=development_dependencies
        )

    def __each_dep(self, data):
        deps_block = re.search(r"defp\s+deps(.+?)\bend\b", data, re.S)
        yield from (dep.group(1) for dep in re.finditer(r"{(.+?)}", deps_block.group(1)))
