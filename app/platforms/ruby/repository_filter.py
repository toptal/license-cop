import re

from app.dependency import *
from app.repository_filter import *

GEMFILE = 'Gemfile'


class RubyRepositoryFilter(RepositoryFilter):

    def match(self, repository):
        return repository.path_exists(GEMFILE)

    def filter_dependencies(self, repository):
        gemfile = repository.read_text_file(GEMFILE)
        dependencies = []

        for line in gemfile.splitlines():
            name = self.__parse_line(line)
            if name:
                dependency = self.__build_dependency(name)
                dependencies.append(dependency)

        return dependencies

    def __parse_line(self, line):
        m = re.match("^\s*gem\s+['\"]([\w\-]+)['\"]", line)
        return m.group(1) if m else None

    def __build_dependency(self, name):
        # For now, we're assuming all dependencies as runtime
        # But we need to parse the Gemfile properly to figure this out
        # We're also ignoring version numbers
        return Dependency(name, Dependency.RUNTIME)
