from collections import deque

from app.dependency_resolution import *


class DependencyResolver:
    def __init__(self, repository):
        self.__repository = repository

    def resolve_version(self, resolution_kind, name, number):
        root = self.__build_node(name, number)

        visited_dependencies = set()
        nodes_to_expand = deque([root])

        while nodes_to_expand:
            current_node = nodes_to_expand.popleft()
            for dependency in current_node.dependencies(resolution_kind):
                child = self.__build_node(dependency.name)
                current_node.add_child(child)
                if dependency not in visited_dependencies:
                    visited_dependencies.add(dependency)
                    nodes_to_expand.append(child)

        return root

    def __build_node(self, name, number=None):
        if number is not None:
            version = self.__repository.fetch_version(name, number)
        else:
            version = self.__repository.fetch_latest_version(name)
        return DependencyResolution(version)
