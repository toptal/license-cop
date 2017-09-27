import sys
import requests

from app.dependency_resolver import *
from app.package_registry import *
from app.package_descriptor_resolution import *


class Platform:
    def __init__(self, name, matcher, registry):
        self.name = name
        self.__matcher = matcher
        self.__registry = registry

    def match(self, repository):
        return self.__matcher.match(repository)

    def resolve(self, match, report):
        resolutions = []
        for i in match.package_descriptors():
            r = self.__resolve_package_descriptor(i)
            resolutions.append(r)
            self.__report_resolution(r, report)
        return resolutions

    def __report_resolution(self, resolution, report):
        print(repr(resolution), file=report)
        print('-' * 70, file=report)
        print(file=report)

    def __resolve_package_descriptor(self, descriptor):
        resolver = DependencyResolver(self.__registry)
        return PackageDescriptorResolution(
            descriptor,
            runtime_resolutions=self.__resolve_dependencies(
                resolver, descriptor.runtime_dependencies),
            development_resolutions=self.__resolve_dependencies(
                resolver, descriptor.development_dependencies)
        )

    def __resolve_dependencies(self, resolver, dependencies):
        resolutions = []
        for dependency in dependencies:
            print('  ▶︎ {0}'.format(dependency))
            resolution = resolver.resolve(dependency)
            resolutions.append(resolution)
        return resolutions
