import re

from app.dependency import *
from app.repository_matcher import *
from app.package_descriptor import *


DEPS_BLOCK_REGEX = re.compile(r'defp?\s+deps(.+?)\bend\b', re.S)
DEPENDENCY_REGEX = re.compile(r'{(.+?)}')
DEVELOPMENT_ENVIRONMENTS = (':dev', ':test', ':docs')


class ElixirRepositoryMatcher(RepositoryMatcher):

    def __init__(self):
        super().__init__(['mix.exs'])

    def _fetch_package_descriptor(self, repository, match):
        mixfile = match.paths[0]

        runtime_dependencies = []
        development_dependencies = []

        data = repository.read_text_file(mixfile)
        for dep in self.__each_dependency(data):
            name, version, *options = [s.strip() for s in dep.split(',', 2)]
            package_name = name[1:]

            if options and any(env in options[0] for env in DEVELOPMENT_ENVIRONMENTS):
                development_dependencies.append(Dependency.development(package_name))
            else:
                runtime_dependencies.append(Dependency.runtime(package_name))

        return PackageDescriptor(
            platform='Elixir',
            repository=repository,
            paths=match.paths,
            runtime_dependencies=runtime_dependencies,
            development_dependencies=development_dependencies
        )

    def __each_dependency(self, data):
        deps_block = DEPS_BLOCK_REGEX.search(data)
        yield from (dep.group(1) for dep in DEPENDENCY_REGEX.finditer(deps_block.group(1)))
