import re

from app.dependency import *
from app.repository_matcher import *
from app.package_descriptor import *
from app.platforms.ios.podfile_parser import PodfileParser


class IosRepositoryMatcher(RepositoryMatcher):

    def __init__(self):
        super().__init__([PackageDescriptorPattern.one_file('podfile', 'Podfile')])

    def _fetch_package_descriptor(self, repository, pattern_match):
        assert len(pattern_match.paths) == 1
        podfile = pattern_match.paths[0]

        data = repository.read_text_file(podfile)

        dependencies = []
        for name in PodfileParser().get_pod_names(data):
            dependency = self.__build_dependency(name)
            dependencies.append(dependency)

        return PackageDescriptor(
            platform='iOS',
            repository=repository,
            paths=[podfile],
            runtime_dependencies=dependencies,
            development_dependencies=[]  # TODO
        )

    def __build_dependency(self, name):
        return Dependency.runtime(name)
