import sys
import requests

from app.dependency_resolver import *
from app.package_registry import *
from app.package_descriptor_resolution import *


class Platform:
    def __init__(self, name, matcher, registry):
        self.name = name
        self.__matcher = matcher
        self.__dependency_resolver = DependencyResolver(registry)

    def match(self, repository):
        return self.__matcher.match(repository)

    def resolve(self, match):
        return list(map(
            lambda i: self.__resolve_package_descriptor(i),
            match.package_descriptors()
        ))

    def __resolve_package_descriptor(self, descriptor):
        return PackageDescriptorResolution(
            descriptor,
            runtime_resolutions=self.__resolve_dependencies(
                descriptor.runtime_dependencies),
            development_resolutions=self.__resolve_dependencies(
                descriptor.development_dependencies)
        )

    def __resolve_dependencies(self, dependencies):
        resolutions = []
        for dependency in dependencies:
            try:
                resolutions.append(self.__dependency_resolver.resolve(dependency))
            except PackageVersionNotFound as e:
                print('WARNING: {0}'.format(e), file=sys.stderr)
        return resolutions
