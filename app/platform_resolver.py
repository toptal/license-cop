from app.dependency_resolver import *


class PlatformResolver:
    def __init__(self, name, repository_filter, package_registry):
        self.name = name
        self.__repository_filter = repository_filter
        self.__dependency_resolver = DependencyResolver(package_registry)

    def match(self, repository):
        return self.__repository_filter.match(repository)

    def resolve(self, repository):
        dependencies = self.__repository_filter.extract_dependencies(repository)
        resolutions = []
        for dependency in dependencies:
            resolutions.append(self.__dependency_resolver.resolve(dependency))
        return resolutions
