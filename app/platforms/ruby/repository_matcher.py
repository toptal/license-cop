import re

from app.dependency import *
from app.repository_matcher import *
from app.manifest import *


class RubyRepositoryMatcher(RepositoryMatcher):

    def __init__(self):
        super().__init__(['Gemfile'])

    def _fetch_manifest(self, repository, match):
        gemfile = match.paths[0]

        data = repository.read_text_file(gemfile)
        dependencies = []

        for line in data.splitlines():
            name = self.__parse_line(line)
            if name:
                dependency = self.__build_dependency(name)
                dependencies.append(dependency)

        return Manifest(
            platform='Ruby',
            repository=repository,
            paths=match.paths,
            runtime_dependencies=dependencies,
            development_dependencies=[]  # TODO
        )

    def __parse_line(self, line):
        m = re.match(r'^\s*gem\s+[\'"]([\w\-]+)[\'"]', line)
        return m.group(1) if m else None

    def __build_dependency(self, name):
        # TODO: for now, we're assuming all dependencies as runtime
        # But we need to parse the Gemfile properly to figure this out
        return Dependency.runtime(name)
