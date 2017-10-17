import re

from app.dependency import *
from app.repository_matcher import *
from app.package_descriptor import *
from app.platforms.ios.podfile_parser import PodfileParser
from app.platforms.ios.podspec_parser import PodspecParser


PODFILE_PATTERN = 'Podfile'
PODSPEC_PATTERN = '*.podspec'


class IosRepositoryMatcher(RepositoryMatcher):

    def __init__(self):
        super().__init__([PODFILE_PATTERN, PODSPEC_PATTERN])

    def _fetch_package_descriptor(self, repository, match):
        dependencies = set()
        for node in match.nodes:
            data = repository.read_text_file(node.path)
            parser = self.__get_parser(node)
            for name in parser.parse(data):
                dependency = self.__build_dependency(name)
                dependencies.add(dependency)

        return PackageDescriptor(
            platform='iOS',
            repository=repository,
            paths=match.paths,
            runtime_dependencies=dependencies,
            development_dependencies=[]
        )

    def __build_dependency(self, name):
        return Dependency.runtime(name)

    def __get_parser(self, node):
        if self.__podfile(node):
            return PodfileParser()
        elif self.__podspec(node):
            return PodspecParser()
        else:
            raise RuntimeError(f'Unrecognized node: {node}')

    def __podfile(self, node):
        return node.match(PODFILE_PATTERN)

    def __podspec(self, node):
        return node.match(PODSPEC_PATTERN)
