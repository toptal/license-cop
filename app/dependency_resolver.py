from collections import deque

from app.dependency_resolution import *


class DependencyResolver:
    def __init__(self, registry):
        self.__registry = registry
        self.__visited_dependencies = set()

    def resolve(self, dependency, runtime_only=False):
        root = self.__build_node(dependency)

        nodes_to_expand = deque([root])

        while nodes_to_expand:
            current_node = nodes_to_expand.popleft()
            for dependency in current_node.dependencies(runtime_only):
                child = self.__build_node(dependency)
                current_node.add_child(child)

                if child.has_dependencies(runtime_only):
                    if dependency not in self.__visited_dependencies:
                        self.__visited_dependencies.add(dependency)
                        nodes_to_expand.append(child)
                    else:
                        child.hide()

        return root

    def __build_node(self, dependency):
        try:
            version = self.__fetch_version(dependency)
        except PackageVersionNotFoundError as e:
            version = PackageVersionNotFound(dependency.name, dependency.number)
        return DependencyResolution(version, dependency.kind)

    def __fetch_version(self, dependency):
        if dependency.number is not None:
            return self.__registry.fetch_version(dependency.name, dependency.number)
        else:
            return self.__registry.fetch_latest_version(dependency.name)
